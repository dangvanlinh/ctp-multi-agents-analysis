"""Knowledge base loader."""

import os
import glob


def load_knowledge(knowledge_dir="knowledge"):
    """Đọc tất cả .md files trong knowledge/ → ghép thành 1 string."""
    knowledge = ""
    files = sorted(glob.glob(os.path.join(knowledge_dir, "*.md")))
    if not files:
        print(f"⚠️  Không tìm thấy file nào trong {knowledge_dir}/")
        return ""

    for f in files:
        name = os.path.basename(f)
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        knowledge += f"\n\n{'='*60}\n📄 {name}\n{'='*60}\n{content}"
        print(f"  Loaded: {name} ({len(content)} chars)")

    return knowledge
