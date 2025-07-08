# College Feedback Classifier (Hugging Face Chat API)

Automatically categorize student feedback using Large Language Models (LLMs) from Hugging Face, via their OpenAI-compatible Chat API (`huggingface_hub.InferenceClient`).  
Built with [Streamlit](https://streamlit.io/) for an interactive, no-code experience.

## ✨ Features

- **Flexible Classification:** Categorize feedback into custom categories (e.g., Academics, Facilities, Administration, Other).
- **Few-shot Learning:** Add example feedback for each category to guide the model ("few-shot" prompting).
- **CSV Upload:** Upload a CSV file with open-ended feedback (CSV must have a `feedback` column).
- **Batch Processing:** Automatically classifies all feedback rows in one click.
- **Download Results:** Download the classified feedback as a new CSV.
- **Model Choice:** Use any supported Hugging Face chat/instruct model (e.g., `Qwen/Qwen2-7B-Instruct`, `meta-llama/Llama-3-8B-Instruct`).
- **No-code UI:** Everything works via a web interface—no coding required by the user!

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/college-feedback-classifier.git
cd college-feedback-classifier
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or, if you don’t have a `requirements.txt`, install manually:

```bash
pip install streamlit pandas huggingface_hub
```

### 3. Get a Hugging Face Access Token

- Sign up at [Hugging Face](https://huggingface.co/join) if you don’t have an account.
- Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and **create a token** with "read" permissions.

### 4. Run the app

```bash
streamlit run college_feedback_classifier_hfhub.py
```

### 5. Use the App

1. **Paste your Hugging Face token** and model id (e.g., `Qwen/Qwen2-7B-Instruct`).
2. **Choose or add categories**.
3. **Provide at least one example feedback per category.**
4. **Upload your feedback CSV** (must have a `feedback` column).
5. **Click "Classify Feedback"** to process.
6. **Download the results** as a CSV with the predicted categories.

---

## 📋 Example: Input CSV

```csv
feedback
The classrooms are always clean and tidy.
I had trouble enrolling for my elective courses.
The food in the cafeteria could be better.
My advisor helped me select the right subjects.
The sports ground lacks proper lighting.
The exam schedule was well organized.
```

## ⚡️ Supported Models

Any Hugging Face model that supports the **OpenAI-compatible Chat API** (e.g., `Qwen/Qwen2-7B-Instruct`, `meta-llama/Llama-3-8B-Instruct`, etc).  
Some models may require you to request access on their Hugging Face page.

## 📝 Project Structure

```
college-feedback-classifier/
│
├── college_feedback_classifier_hfhub.py   # Main Streamlit app
├── requirements.txt
├── README.md
```

## 🛠️ Advanced

- You can set your Hugging Face token as an environment variable (`HF_TOKEN`) for non-Streamlit scripts.
- For API/batch use, adapt the `chat_classify_feedback` function in the main app.

## 🙏 Attribution

- Built using [Streamlit](https://streamlit.io/), [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub/index), and open LLMs.
- Inspired by the power of open-source LLMs for practical, no-code AI solutions.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---
```
