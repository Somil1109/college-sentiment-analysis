import streamlit as st
import pandas as pd
import os
from huggingface_hub import InferenceClient

st.set_page_config(page_title="College Feedback Classifier (huggingface_hub)", layout="wide")

st.title("🎓 College Feedback Classifier (HuggingFace Hub - Chat API)")

st.markdown("""
This app uses the Hugging Face Hub's InferenceClient (`provider="auto"`) and OpenAI-compatible Chat API.
You can use models like `Qwen/Qwen2-7B-Instruct`, `meta-llama/Llama-3-8B-Instruct`, etc.
""")

# Sidebar for configuration
st.sidebar.header("Configuration")

categories = st.sidebar.multiselect(
    "Set Categories",
    ["Academics", "Facilities", "Administration", "Other"],
    default=["Academics", "Facilities", "Administration", "Other"]
)

hf_token = st.sidebar.text_input(
    "Hugging Face Token",
    help="Get your token at https://huggingface.co/settings/tokens",
    type="password"
)
model_id = st.sidebar.text_input(
    "Model ID",
    value="Qwen/Qwen2-7B-Instruct",
    help="Example: Qwen/Qwen2-7B-Instruct, meta-llama/Llama-3-8B-Instruct"
)

st.markdown("### 1. Define Few-Shot Examples")
st.info("Provide at least one example per category. These help the model learn classification logic.")

examples = []
for cat in categories:
    example = st.text_area(f"Example feedback for `{cat}`", key=f"ex-{cat}")
    if example:
        examples.append({"text": example, "label": cat})

if len(examples) < len(categories):
    st.warning("Please provide at least one example for each category.")

st.markdown("### 2. Upload Student Feedback CSV")
st.caption("CSV must have a column named `feedback` containing the open-ended student feedback.")

uploaded_file = st.file_uploader("Upload Feedback CSV", type=["csv"])

def chat_classify_feedback(feedback, categories, examples, client, model_id):
    prompt = (
        "Classify the following student feedback as one of these categories: "
        + ", ".join(categories) + ".\n\n"
    )
    for ex in examples:
        prompt += f'Feedback: "{ex["text"]}"\nCategory: {ex["label"]}\n\n'
    prompt += f'Feedback: "{feedback}"\nCategory:'
    messages = [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        output = completion.choices[0].message.content.strip()
        # Try to extract only the category name
        output = output.split("Category:")[-1].strip().split("\n")[0]
        for cat in categories:
            if cat.lower() in output.lower():
                return cat
        return output
    except Exception as e:
        return f"API_EXCEPTION: {e}"

def batch_classify_chat(df, categories, examples, client, model_id):
    results = []
    for feedback in df['feedback']:
        label = chat_classify_feedback(feedback, categories, examples, client, model_id)
        results.append(label)
    return results

# Show token if desired
if st.sidebar.checkbox("Show Hugging Face Token", value=False):
    st.sidebar.write(f"**Token:** {hf_token}")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'feedback' not in df.columns:
        st.error("CSV must contain a column named 'feedback'.")
        st.stop()
    st.write("Sample Data:", df.head())

    if st.button("Classify Feedback"):
        if not (hf_token and model_id and len(examples) == len(categories)):
            st.error("Please fill in all Hugging Face API credentials and provide examples for every category.")
            st.stop()
        with st.spinner("Classifying... (may take a while for large files)"):
            # Set up InferenceClient
            client = InferenceClient(provider="auto", api_key=hf_token)
            df["category"] = batch_classify_chat(df, categories, examples, client, model_id)
        st.success("Classification complete!")
        st.dataframe(df)

        st.markdown("### 3. Category Insights")
        st.bar_chart(df["category"].value_counts())

        st.download_button(
            "Download Classified Feedback as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="classified_feedback.csv",
            mime="text/csv"
        )
else:
    st.info("Upload a CSV file with a `feedback` column to start.")

st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit & huggingface_hub. "
    "For best results, use a chat/instruct LLM model."
)
