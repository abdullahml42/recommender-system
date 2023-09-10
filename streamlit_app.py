import streamlit as st

from test import RecommendProducts


def display_header():
    """Displays the header."""
    st.header("Scientific Product Recommender System")


def get_reviewer_id():
    """Returns the reviewer ID."""
    suggested_ids = ["", "A0096681Y127OL1H8W3U", "AKX9EQ37PAYMY", "A2ZRAUZCUHW66X"]
    reviewer_id = st.selectbox("Select or Enter User ID:", suggested_ids)

    if reviewer_id == "":
        reviewer_id = st.text_input("Enter User ID:")
    else:
        reviewer_id = reviewer_id if reviewer_id != "" else None

    return reviewer_id


def get_number_of_items():
    """Returns the number items for recommendations."""
    num_items = st.text_input("Enter Number of Items:", value="5")
    return num_items


def recommend_products(reviewer_id, num_items):
    """Recommends products for a given reviewer ID with a specified number of items."""
    recommender = RecommendProducts(reviewer_id)

    try:
        num_items = int(num_items)
    except ValueError:
        st.error("Invalid input for number of items. Please enter an integer.")
        return

    try:
        recommendations = recommender.recommend_products(num_items)

        if not recommendations.empty:
            st.header("Recommendations")
            recommendations = recommendations.rename(
                columns={
                    "recommendedProductID": "Product ID",
                    "predictedRating": "Predicted Rating"
                }
            )

            html = recommendations.to_html(index=False)
            st.write(html, unsafe_allow_html=True)
        else:
            st.info("No recommendations found for the given user.")
    except ValueError as e:
        if "contains previously unseen labels" in str(e):
            st.info("No recommendations found for the given user.")
        else:
            st.error(str(e))


def main():
    """Orchestrates the program flow."""
    display_header()
    reviewer_id = get_reviewer_id()
    num_items = get_number_of_items()
    recommend_button = st.button("Recommend Products")

    if recommend_button:
        if reviewer_id:
            recommend_products(reviewer_id, num_items)
        else:
            st.warning("Please select or enter a valid User ID.")


if __name__ == "__main__":
    main()
