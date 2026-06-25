"""BookMind — 密钥授权系统 (D)"""
import hashlib
import hmac
import json
import os
import platform
import uuid

SECRET_KEY = os.environ.get("BOOKMIND_SECRET", hashlib.sha256(b"BookMind:v1").hexdigest()[:32])
LICENSE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".license")

def get_machine_id() -> str:
    """生成唯一机器标识"""
    try:
        # 尝试获取稳定的硬件ID
        info = [
            platform.node(),
            platform.processor() or "unknown",
            uuid.getnode(),  # MAC address based
        ]
        raw = "-".join(str(x) for x in info)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    except:
        return "unknown"

def generate_license(level: str = "pro") -> str:
    """生成授权码（管理员用）"""
    machine = get_machine_id()
    payload = f"{machine}:{level}:BookMind"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()[:8]
    license_key = f"BM-{level.upper()}-{machine[:8]}-{sig}"
    return license_key

def validate_license(license_key: str = None) -> dict:
    """验证授权码"""
    if license_key is None:
        license_key = _load_license()
    
    if not license_key:
        return {"valid": False, "level": "free", "reason": "未激活"}
    
    try:
        parts = license_key.split("-")
        if len(parts) != 4 or parts[0] != "BM":
            return {"valid": False, "level": "free", "reason": "格式错误"}
        
        level = parts[1].lower()
        mid = parts[2]
        sig = parts[3]
        
        machine = get_machine_id()
        payload = f"{machine}:{level}:BookMind"
        expected_sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()[:8]
        
        if sig != expected_sig and mid != machine[:8]:
            # 兼容旧格式
            payload2 = f"{mid}:{level}:BookMind"
            expected_sig2 = hmac.new(SECRET_KEY.encode(), payload2.encode(), hashlib.sha256).hexdigest()[:8]
            if sig != expected_sig2:
                return {"valid": False, "level": "free", "reason": "授权码无效"}
        
        level_name = {"free": "免费版", "pro": "专业版", "enterprise": "企业版"}.get(level, "免费版")
        return {"valid": True, "level": level, "level_name": level_name}
    except Exception as e:
        return {"valid": False, "level": "free", "reason": f"验证异常: {e}"}

def _load_license() -> str:
    """从文件加载授权码"""
    try:
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, 'r') as f:
                return f.read().strip()
    except:
        pass
    return ""

def save_license(license_key: str) -> bool:
    """保存授权码"""
    try:
        with open(LICENSE_FILE, 'w') as f:
            f.write(license_key.strip())
        return True
    except:
        return False

def get_license_status() -> dict:
    """获取当前授权状态"""
    key = _load_license()
    return validate_license(key)

# 免费版限制
FREE_LIMITS = {
    "max_file_size_mb": 5,
    "max_chunks_per_book": 10,
    "insights_per_day": 3,
    "show_ads": True,
}

PRO_LIMITS = {
    "max_file_size_mb": 100,
    "max_chunks_per_book": 999,
    "insights_per_day": 999,
    "show_ads": False,
}

def get_limits() -> dict:
    """获取当前可用限制"""
    status = get_license_status()
    if status.get("level") in ("pro", "enterprise"):
        return PRO_LIMITS
    return FREE_LIMITS
