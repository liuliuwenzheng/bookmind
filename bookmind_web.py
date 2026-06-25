#!/usr/bin/env python3
"""BookMind Web — Streamlit 图形界面 (C)
📚 上传 → 阅读 → AI 总结 → 洞见提取 → 技能卡片
"""
import streamlit as st
import os
import sys
import tempfile
import time

base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base)

from src.reader import read_file, chunk_text
from src.ai import AIEngine
from src.license import validate_license, save_license, get_license_status, get_limits, generate_license

st.set_page_config(
    page_title="BookMind 📚 AI 读书助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== Sidebar: License / About =====
with st.sidebar:
    st.title("📚 BookMind")
    st.markdown("让每本书都长出知识的翅膀 🧠")
    st.divider()
    
    # License section
    st.subheader("🔑 授权管理")
    lic_status = get_license_status()
    if lic_status["valid"]:
        st.success(f"✅ {lic_status['level_name']}")
    else:
        st.warning(f"⚠️ {lic_status['level_name']} - {lic_status['reason']}")
        lic_input = st.text_input("输入授权码", type="password", key="lic_input")
        if st.button("激活", key="act_btn"):
            result = validate_license(lic_input)
            if result["valid"]:
                save_license(lic_input)
                st.success(f"✅ 已激活 {result['level_name']}！")
                st.rerun()
            else:
                st.error(f"❌ {result['reason']}")
    
    limits = get_limits()
    st.caption(f"📎 最大文件: {limits['max_file_size_mb']}MB")
    st.caption(f"📄 最多章节: {limits['max_chunks_per_book']}")
    
    st.divider()
    st.caption("BookMind v1.0 © 2026")

# ===== Main Area =====
st.title("📖 BookMind AI 读书助手")
st.markdown("上传电子书，让 AI 帮你阅读、总结、提取知识！")

# Tabs
tab_read, tab_summarize, tab_insights, tab_skill, tab_admin = st.tabs([
    "📖 阅读", "📋 总结", "💡 洞见", "🛠 技能卡片", "⚙️ 管理"
])

# Initialize AI engine
@st.cache_resource
def get_ai():
    return AIEngine()

ai = get_ai()

# Session state for book text
if "book_text" not in st.session_state:
    st.session_state.book_text = ""
if "book_name" not in st.session_state:
    st.session_state.book_name = ""
if "chunks" not in st.session_state:
    st.session_state.chunks = []

def load_book(uploaded_file):
    """Load and parse uploaded book"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    try:
        text = read_file(tmp_path)
        st.session_state.book_text = text
        st.session_state.book_name = uploaded_file.name
        
        limits = get_limits()
        chunks = chunk_text(text, max_chars=3000)[:limits["max_chunks_per_book"]]
        st.session_state.chunks = chunks
        
        return True, len(text), len(chunks)
    except Exception as e:
        return False, str(e), 0
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

# ===== Upload Area =====
uploaded_file = st.file_uploader(
    "📤 选择电子书文件",
    type=["epub", "pdf", "txt", "md", "markdown"],
    help="支持 EPUB / PDF / TXT / Markdown 格式"
)

if uploaded_file is not None:
    # Check file size
    limits = get_limits()
    if uploaded_file.size > limits["max_file_size_mb"] * 1024 * 1024:
        st.error(f"❌ 文件过大！免费版限制 {limits['max_file_size_mb']}MB，请升级到专业版。")
    else:
        if st.button("📂 加载此书", type="primary", key="load_btn"):
            with st.spinner("🔄 正在解析..."):
                success, info, nchunks = load_book(uploaded_file)
                if success:
                    st.success(f"✅ 已加载 {uploaded_file.name} ({info/1024:.0f} KB, {nchunks} 章节)")
                else:
                    st.error(f"❌ 读取失败: {info}")

# ===== Tab 1: Read =====
with tab_read:
    st.subheader("📖 阅读模式")
    if st.session_state.book_text:
        chunk_idx = st.select_slider(
            "章节导航",
            options=range(len(st.session_state.chunks)),
            format_func=lambda i: f"章节 {i+1}/{len(st.session_state.chunks)}"
        )
        st.text_area(
            f"📄 {st.session_state.book_name} — 章节 {chunk_idx+1}",
            st.session_state.chunks[chunk_idx],
            height=500,
            disabled=True,
        )
        st.caption(f"📊 全书 {len(st.session_state.book_text):,} 字 · {len(st.session_state.chunks)} 章节")
    else:
        st.info("📂 请先上传一本书")

# ===== Tab 2: Summarize =====
with tab_summarize:
    st.subheader("📋 AI 总结")
    if st.session_state.chunks:
        col1, col2 = st.columns([3, 1])
        with col1:
            summary_style = st.selectbox("总结风格", ["详细", "简洁", "一句话"])
        with col2:
            if st.button("🤖 生成总结", type="primary", use_container_width=True):
                with st.spinner("🔄 AI 正在思考..."):
                    text = "\n\n".join(st.session_state.chunks)
                    result = ai.summarize(text[:3000], max_length=summary_style)
                    st.markdown("### 📋 总结结果")
                    st.markdown(result)
                    st.divider()
                    st.caption("🤖 由本地 LM Studio AI 生成")
    else:
        st.info("📂 请先上传一本书")

# ===== Tab 3: Insights =====
with tab_insights:
    st.subheader("💡 知识洞见")
    if st.session_state.chunks:
        if st.button("🔍 提取洞见", type="primary"):
            with st.spinner("🔄 AI 正在分析..."):
                text = "\n\n".join(st.session_state.chunks[:3])
                result = ai.extract_insights(text[:2800])
                st.markdown("### 💡 核心洞见")
                st.markdown(result)
                st.divider()
                st.caption("🤖 由本地 LM Studio AI 生成")
    else:
        st.info("📂 请先上传一本书")

# ===== Tab 4: Skill Card =====
with tab_skill:
    st.subheader("🛠 技能卡片生成")
    if st.session_state.chunks:
        if st.button("🎴 生成技能卡片", type="primary"):
            with st.spinner("🔄 AI 正在提炼..."):
                text = "\n\n".join(st.session_state.chunks[:3])
                result = ai.generate_skill_card(text[:2500])
                st.markdown("### 🛠 技能卡片")
                st.markdown(result)
                st.divider()
                # Export option
                if st.button("📥 保存为 Markdown"):
                    skill_path = os.path.join(base, "examples", f"skill_{st.session_state.book_name}.md")
                    with open(skill_path, 'w', encoding='utf-8') as f:
                        f.write(f"# 技能卡片: {st.session_state.book_name}\n\n{result}")
                    st.success(f"✅ 已保存到 {skill_path}")
                st.caption("🤖 由本地 LM Studio AI 生成")
    else:
        st.info("📂 请先上传一本书")

# ===== Tab 5: Admin =====
with tab_admin:
    st.subheader("⚙️ 管理面板")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔑 生成授权码")
        if st.button("🔄 生成本机授权码"):
            lic = generate_license("pro")
            st.code(lic, language="text")
            st.info("将此授权码复制到授权输入框激活专业版")
    
    with col2:
        st.markdown("### 📊 使用统计")
        if st.session_state.book_text:
            st.metric("已加载书籍", st.session_state.book_name)
            st.metric("总字数", f"{len(st.session_state.book_text):,}")
            st.metric("章节数", len(st.session_state.chunks))
        else:
            st.info("暂未加载书籍")
    
    st.divider()
    st.markdown("### 📦 系统信息")
    st.json({
        "AI 引擎": ai.model,
        "API 地址": ai.api_base,
        "授权状态": get_license_status(),
        "文件大小限制": f"{limits['max_file_size_mb']}MB",
    })

# Footer
st.divider()
st.caption("BookMind — 让每本书都长出知识的翅膀 🧠📚 | 基于 LM Studio 本地 AI")
