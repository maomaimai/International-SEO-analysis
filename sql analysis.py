import sqlite3
import pandas as pd

# reconnect to the database
conn = sqlite3.connect('seo_analytics.db')

# SQL Inquiries
sql_query = """
WITH RankedKeywords AS (
    -- 1. Firstly, Inquiry about the total impressions, conversions and revenues of different region
    SELECT 
        region,
        language,
        keyword,
        SUM(impressions) as total_impressions,
        SUM(clicks) as total_clicks,
        SUM(conversions) as total_conversions,
        SUM(revenue_usd) as total_revenue,
        AVG(page_load_time_sec) as avg_load_time,
        -- Using ROW_NUMBER() window function
        ROW_NUMBER() OVER (
            PARTITION BY region, language 
            ORDER BY SUM(clicks) DESC
        ) as click_rank
    FROM traffic_data
    GROUP BY region, language, keyword
)
-- 2. 2. Filter out the top 3 core keywords globally by clicks, and use CASE WHEN to mark which ones have a 'speed crisis'.
SELECT 
    region,
    language,
    keyword,
    total_clicks,
    total_revenue,
    ROUND(avg_load_time, 2) as avg_load_time_sec,
    click_rank,
    -- Business logic rule: Exceeding 4 seconds is a critical red line for user churn by US e-commerce standards.
    CASE 
        WHEN avg_load_time > 5.0 THEN '🔴 Severe Latency (High Revenue Risk)'
        WHEN avg_load_time BETWEEN 3.0 AND 5.0 THEN '🟡 Moderate Latency'
        ELSE '🟢 Healthy Speed'
    END as site_health_status
FROM RankedKeywords
WHERE click_rank <= 3
ORDER BY region DESC, language, click_rank;
"""

# using pandas to clearly present the sql analysis result
sql_result = pd.read_sql_query(sql_query, conn)


print("\n🔥 SQL analysis core results(Partial):")
print(sql_result.to_string(index=False))

# close database
conn.close()
