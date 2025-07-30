import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load Dataset
def load_product_dataset():
    # You can replace this with a CSV read for larger dataset
    data = {
        'ID': range(1, 11),
        'Name': [
            'Liquid Dish Soap', 'Toilet Cleaner', 'Laundry Detergent', 'Glass Cleaner',
            'Floor Mop', 'Air Freshener', 'Fabric Softener', 'Window Wiper',
            'Kitchen Towel', 'Bleach Disinfectant'
        ],
        'Description': [
            'cleaning kitchen liquid soap lemon',
            'bathroom cleaning toilet disinfectant bleach',
            'laundry washing clothes detergent stain remover',
            'glass window cleaner shine spray alcohol',
            'floor mop cleaning dust wood washable',
            'air freshener room smell fragrance lavender',
            'clothes soft fabric conditioner fresh scent',
            'window wiper rubber handle glass cleaning tool',
            'kitchen towel paper absorbent cooking wipe',
            'strong bleach disinfectant cleaner germs remover'
        ],
        'Category': [
            'Kitchen', 'Bathroom', 'Laundry', 'Windows', 'Floor',
            'Air Care', 'Laundry', 'Windows', 'Kitchen', 'Bathroom'
        ]
    }

    return pd.DataFrame(data)

# Step 2: Preprocess text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# Step 3: Generate TF-IDF Matrix using Name + Description
def generate_feature_matrix(df):
    combined_text = (df['Name'] + ' ' + df['Description']).apply(preprocess)
    tfidf = TfidfVectorizer(stop_words='english')
    return tfidf.fit_transform(combined_text)

# Step 4: Compute cosine similarity
def compute_similarity_matrix(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)

# Step 5: Recommend products
def recommend_similar_products(input_name, product_df, similarity_matrix, top_n=5):
    # Case-insensitive exact or partial match
    input_name = input_name.lower()
    matches = product_df[product_df['Name'].str.lower().str.contains(input_name)]

    if matches.empty:
        raise ValueError(f"No matching product found for: {input_name}")

    target_index = matches.index[0]  # Take the first match
    similarity_scores = list(enumerate(similarity_matrix[target_index]))

    # Sort and exclude itself
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in similarity_scores if i != target_index][:top_n]

    return product_df.iloc[top_indices][['Name', 'Category', 'Description']]

# Main Execution
def main():
    df = load_product_dataset()
    tfidf_features = generate_feature_matrix(df)
    similarity_matrix = compute_similarity_matrix(tfidf_features)

    while True:
        try:
            product_input = input("Enter a product name (or 'exit' to quit): ").strip()
            if product_input.lower() == 'exit':
                break

            recommendations = recommend_similar_products(product_input, df, similarity_matrix)
            print(f"\nTop recommendations for '{product_input}':\n")
            print(recommendations.to_string(index=False))
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
