#!/usr/bin/env python3
"""BookMind — 让每本书都长出知识的翅膀 🧠📚

结合本地 LM Studio (Gemma/Gemini) 的 AI 电子书阅读器。
支持 EPUB / PDF / TXT / Markdown，生成总结、洞见、技能卡片。

用法:
  python bookmind.py read 书籍.epub         → 阅读 + 章节总结
  python bookmind.py summarize 书籍.pdf      → AI 总结全书
  python bookmind.py insights 书籍.txt       → 提取关键洞见
  python bookmind.py skill 书籍.epub         → 生成技能卡片
  python bookmind.py serve                   → 启动 Web API 服务 (待实现)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.reader import read_file, chunk_text
from src.ai import AIEngine

def cmd_summarize(args):
    """Summarize a book."""
    path = args[0]
    print(f"📖 正在读取: {path}")
    text = read_file(path)
    chunks = chunk_text(text, max_chars=2800)
    
    ai = AIEngine()
    
    if len(chunks) == 1:
        print("🤖 正在生成总结...")
        result = ai.summarize(chunks[0])
        print("\n" + "="*50)
        print(result)
        print("="*50)
    else:
        # Multi-chunk: summarize each, then summarize summaries
        print(f"📚 全书共 {len(chunks)} 个章节，正在逐章总结...")
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"  📝 章节 {i+1}/{len(chunks)}...")
            s = ai.summarize(chunk, max_length="简洁")
            summaries.append(f"## 章节 {i+1}\n{s}")
        
        print("\n🤖 正在生成全书总览...")
        full = ai.summarize("\n\n".join(summaries), max_length="详细")
        print("\n" + "="*50)
        print("📋 全书总结")
        print("="*50)
        print(full)
        
        # Save to file
        out_path = os.path.splitext(os.path.basename(path))[0] + "_总结.md"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"# {os.path.basename(path)} 总结\n\n")
            f.write(full + "\n\n---\n\n")
            f.write("\n\n".join(summaries))
        print(f"\n💾 已保存到: {out_path}")

def cmd_insights(args):
    """Extract insights from a book."""
    path = args[0]
    print(f"📖 正在读取: {path}")
    text = read_file(path)
    chunks = chunk_text(text, max_chars=2500)
    
    ai = AIEngine()
    print("🔍 正在萃取知识...")
    
    all_insights = []
    for i, chunk in enumerate(chunks[:3]):  # Process first 3 chunks
        print(f"  🔬 分析段落 {i+1}/{min(len(chunks), 3)}...")
        result = ai.extract_insights(chunk)
        all_insights.append(result)
    
    print("\n" + "="*50)
    print("💡 知识萃取结果")
    print("="*50)
    for insight in all_insights:
        print(insight)
        print("-"*30)
    
    out_path = os.path.splitext(os.path.basename(path))[0] + "_洞见.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"# {os.path.basename(path)} 知识洞见\n\n")
        f.write("\n\n---\n\n".join(all_insights))
    print(f"\n💾 已保存到: {out_path}")

def cmd_skill(args):
    """Generate a skill card from knowledge."""
    path = args[0]
    print(f"📖 正在读取: {path}")
    text = read_file(path)
    chunks = chunk_text(text, max_chars=2500)
    
    ai = AIEngine()
    print("🃏 正在生成技能卡片...")
    
    result = ai.generate_skill_card(chunks[0])
    print("\n" + "="*50)
    print(result)
    print("="*50)
    
    out_path = os.path.splitext(os.path.basename(path))[0] + "_技能卡片.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\n💾 已保存到: {out_path}")

def cmd_read(args):
    """Read and chapter-summarize."""
    path = args[0]
    print(f"📖 正在阅读: {path}")
    text = read_file(path)
    chunks = chunk_text(text, max_chars=3000)
    
    print(f"📚 共 {len(chunks)} 个章节")
    for i, chunk in enumerate(chunks):
        print(f"\n{'='*50}")
        print(f"📝 章节 {i+1}/{len(chunks)}")
        print(f"{'='*50}")
        # Show first 500 chars of each chapter
        print(chunk[:500])
        if len(chunk) > 500:
            print(f"... (共 {len(chunk)} 字符)")
        
        if i >= 4:  # Show max 5 chapters in read mode
            print(f"\n... 还有 {len(chunks)-i-1} 个章节")
            break

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    file_args = sys.argv[2:]
    
    commands = {
        'read': cmd_read,
        'summarize': cmd_summarize,
        'insights': cmd_insights,
        'skill': cmd_skill,
    }
    
    if command in commands:
        commands[command](file_args)
    else:
        print(f"❌ 未知命令: {command}")
        print(__doc__)
        sys.exit(1)
