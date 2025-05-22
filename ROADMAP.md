# 🔥 FORGE_ROADMAP.md

This roadmap defines the evolution of **The Forge**, from a fine-tuning panel into a full LLM lifecycle interface — empowering users to train, tune, analyze, and deploy custom language models.

---

## 🧱 Phase 1: Split and Scaffold Core Tabs

- [ ] Create **tabbed interface** with two primary views:
    - 🔨 Full Training
    - 🎯 Fine-Tuning
- [ ] Migrate current UI content into **Fine-Tuning** tab
- [ ] Scaffold placeholder layout + YAML config preview in **Full Training** tab
- [ ] Add tab description + tooltips to explain the distinction

---

## 🧬 Phase 2: Full Training MVP

- [ ] Let user upload raw corpus for pretraining (e.g. .txt, .jsonl)
- [ ] Choose base model or start from scratch
- [ ] Basic config form:
    - Epochs, batch size, learning rate
- [ ] Launch `train_runner.py` from frontend
- [ ] Log training output and save model locally

---

## 🎯 Phase 3: Fine-Tuning Upgrade

- [ ] Validate dataset structure (prompt → completion pairs)
- [ ] Add support for multi-format (chat, CSV)
- [ ] Show training impact estimations (token cost, steps, time)
- [ ] Add support for LoRA-based fine-tuning (optional backend)

---

## 🧠 Phase 4: Evaluation & Feedback

- [ ] Add **Evaluation tab**
    - Upload eval set or write test prompts
    - Show output side-by-side across checkpoints
- [ ] Visualize metrics:
    - Diversity
    - Accuracy (if labeled)
    - Output style match
- [ ] Hook into existing compare UI for visualization

---

## 🔁 Phase 5: Iteration Tools

- [ ] Load previous configs and results
- [ ] Fork from previous run
- [ ] Create tuning “branches” for controlled experimentation
- [ ] Allow restore to Codex for prompt-based testing

---

## 📦 Phase 6: Packaging & Export

- [ ] Export model checkpoint + YAML config bundle
- [ ] Add deployment target presets (Hugging Face, Ollama, etc.)
- [ ] Include metadata (author, license, version, tags)

---

## 🧙‍♂️ Phase 7: Learn Mode (Optional)

- [ ] Add collapsible explainer panels for every stage
- [ ] “Did you know?” prompts and tuning tips
- [ ] Inline definitions: temperature, overfitting, batch size
- [ ] Recommended reading / link to LLM 101

---

Let me know when you're ready to turn this into issues, cards, or code scaffolds.