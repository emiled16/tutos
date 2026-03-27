"""Product-level feature engineering."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window


def compute_popularity(
    transactions: DataFrame,
    clickstream: DataFrame,
) -> DataFrame:
    """Compute product popularity scores from purchases and clicks.

    Args:
        transactions: DataFrame with columns [product_id, timestamp].
        clickstream: DataFrame with columns [product_id, event_type, timestamp].

    Returns:
        DataFrame with columns [product_id, purchase_count, view_count,
        click_count, popularity_score].
    """
    # TODO: Implement popularity scoring
    # 1. Count purchases per product from transactions
    # 2. Count views and clicks per product from clickstream
    # 3. Compute popularity_score as weighted combination
    #    (e.g., 0.5 * norm_purchases + 0.3 * norm_clicks + 0.2 * norm_views)
    pass


def compute_price_statistics(
    transactions: DataFrame,
    products: DataFrame,
) -> DataFrame:
    """Compute price-related features per product.

    Args:
        transactions: DataFrame with columns [product_id, amount, quantity].
        products: DataFrame with columns [product_id, price, category].

    Returns:
        DataFrame with columns [product_id, avg_selling_price,
        price_vs_category_avg, discount_frequency].
    """
    # TODO: Implement price statistics
    # 1. Compute avg actual selling price from transactions
    # 2. Compute category average price using window function
    # 3. price_vs_category_avg = product_price / category_avg_price
    # 4. discount_frequency = fraction of sales below list price
    pass


def compute_category_rank(
    transactions: DataFrame,
    products: DataFrame,
) -> DataFrame:
    """Rank products within their category by sales volume.

    Args:
        transactions: DataFrame with columns [product_id, quantity].
        products: DataFrame with columns [product_id, category].

    Returns:
        DataFrame with columns [product_id, category, sales_volume,
        category_rank, category_percentile].
    """
    # TODO: Implement within-category ranking
    # 1. Join transactions with products to get category
    # 2. Compute total sales_volume per product
    # 3. Use dense_rank() window function partitioned by category, ordered by sales_volume desc
    # 4. Compute percentile using percent_rank()
    pass
