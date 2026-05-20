# ================================================================
# INTERVIEW PREPARATION QUESTIONS
# ================================================================
# Author: Business Intelligence Analyst
# Purpose: Comprehensive interview Q&A for BI/Data Analyst roles
# ================================================================

# ================================================================
# PART 1: SQL INTERVIEW QUESTIONS
# ================================================================

## Basic SQL Questions

### Q1: What is the difference between WHERE and HAVING?
**Answer**: WHERE filters rows before aggregation, HAVING filters after GROUP BY. Use WHERE for column-level filtering, HAVING for aggregate filtering.

```sql
-- WHERE example: Filter before grouping
SELECT category, SUM(amount)
FROM sales
WHERE amount > 100
GROUP BY category;

-- HAVING example: Filter after grouping
SELECT category, SUM(amount)
FROM sales
GROUP BY category
HAVING SUM(amount) > 10000;
```

### Q2: What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?
**Answer**:
- ROW_NUMBER(): Assigns unique sequential numbers (1, 2, 3, 4)
- RANK(): Assigns same rank for ties, with gaps (1, 1, 3, 4)
- DENSE_RANK(): Assigns same rank for ties, without gaps (1, 1, 2, 3)

### Q3: What is a CTE? When would you use it?
**Answer**: Common Table Expression (CTE) is a temporary named result set. Use it to:
- Simplify complex queries
- Improve readability
- Reference itself recursively
- Replace nested subqueries

```sql
WITH monthly_sales AS (
    SELECT MONTH(order_date) AS month, SUM(amount) AS revenue
    FROM sales
    GROUP BY MONTH(order_date)
)
SELECT * FROM monthly_sales WHERE revenue > 10000;
```

## Advanced SQL Questions

### Q4: Explain LAG() and LEAD() with examples
**Answer**: Window functions for accessing previous/next row data.

```sql
SELECT 
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_day_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_day_amount
FROM sales;
```

### Q5: How do you calculate running totals in SQL?
**Answer**: Using SUM() OVER() with ORDER BY.

```sql
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM sales;
```

### Q6: What is the difference between INNER JOIN and LEFT JOIN?
**Answer**:
- INNER JOIN: Returns only matching rows from both tables
- LEFT JOIN: Returns all rows from left table, matching rows from right (NULL for no match)

### Q7: How would you handle division by zero in SQL?
**Answer**: Using NULLIF() function.

```sql
SELECT 
    category,
    SUM(amount) / NULLIF(COUNT(*), 0) AS avg_order_value
FROM sales
GROUP BY category;
```

### Q8: Explain COALESCE and its use cases
**Answer**: Returns first non-NULL value from a list. Use for:
- Handling missing values in calculations
- Providing default values
- NULL-safe operations

```sql
SELECT COALESCE(courier_status, 'Pending') FROM sales;
SELECT COALESCE(amount, 0) + COALESCE(shipping, 0) FROM orders;
```

### Q9: How do you find duplicate records?
**Answer**: Using GROUP BY with HAVING COUNT(*) > 1.

```sql
SELECT order_id, COUNT(*) AS cnt
FROM sales
GROUP BY order_id
HAVING COUNT(*) > 1;
```

### Q10: Write a query to find month-over-month growth
**Answer**:
```sql
WITH monthly AS (
    SELECT MONTH(order_date) AS month, SUM(amount) AS revenue
    FROM sales
    GROUP BY MONTH(order_date)
)
SELECT 
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    (revenue - LAG(revenue) OVER (ORDER BY month)) / 
        NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100 AS growth_pct
FROM monthly;
```

### Q11: What is a subquery? When would you use it?
**Answer**: Query nested inside another query. Types:
- Scalar subquery: Returns single value
- Table subquery: Returns table
- Correlated subquery: References outer query

### Q12: How do you optimize SQL queries?
**Answer**:
1. Use proper indexes
2. Avoid SELECT *
3. Use EXISTS instead of IN for large datasets
4. Limit result sets with WHERE clauses
5. Avoid functions on indexed columns
6. Use appropriate JOIN types
7. Minimize subqueries, prefer CTEs

### Q13: Explain window functions vs aggregate functions
**Answer**:
- Aggregate functions: Collapse rows into single value (SUM, AVG, COUNT)
- Window functions: Compute values across related rows without collapsing

```sql
-- Aggregate: Returns single value per group
SELECT category, SUM(amount) FROM sales GROUP BY category;

-- Window: Returns all rows with calculated value
SELECT order_id, SUM(amount) OVER (PARTITION BY category) AS category_total
FROM sales;
```

### Q14: How do you calculate moving average?
**Answer**:
```sql
SELECT 
    order_date,
    amount,
    AVG(amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
FROM sales;
```

### Q15: What is the use of PARTITION BY?
**Answer**: Divides result set into partitions for window function calculations.

```sql
SELECT 
    category,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY category ORDER BY order_date) AS running_total_by_cat
FROM sales;
```

---

# ================================================================
# PART 2: DASHBOARD EXPLANATION QUESTIONS
# ================================================================

### Q16: How do you approach a new dashboard design?
**Answer**: 
1. Understand stakeholder requirements
2. Identify key business questions
3. Gather data sources
4. Define KPIs and metrics
5. Design wireframe/layout
6. Build and iterate based on feedback
7. Document and train users

### Q17: What makes a good dashboard?
**Answer**:
- Clear purpose aligned with audience
- Right KPIs with meaningful metrics
- Simple, uncluttered design
- Intuitive navigation
- Consistent color scheme
- Interactive but not overwhelming
- Fast loading performance
- Mobile responsiveness

### Q18: How do you choose the right chart type?
**Answer**:
| Data Type | Recommended Charts |
|-----------|-------------------|
| Trend over time | Line, Area |
| Category comparison | Bar, Column |
| Part-to-whole | Pie, Donut, Stacked Bar |
| Distribution | Histogram, Box Plot |
| Relationship | Scatter Plot |
| Geographic | Map, Filled Map |
| Ranking | Bar, Treemap |
| Funnel | Funnel Chart |

### Q19: Explain your dashboard design process
**Answer**:
1. **Discovery**: Stakeholder interviews, requirements gathering
2. **Data Assessment**: Source identification, data quality check
3. **KPI Definition**: Metrics that matter for the audience
4. **Wireframing**: Layout sketch, information hierarchy
5. **Development**: Build in Power BI with DAX measures
6. **Testing**: User acceptance testing, performance check
7. **Deployment**: Publish, configure scheduled refresh
8. **Training**: User documentation, walkthrough sessions
9. **Maintenance**: Monitor usage, gather feedback, iterate

### Q20: How do you handle performance issues in dashboards?
**Answer**:
1. Use summarized tables instead of detail tables
2. Implement incremental data refresh
3. Optimize DAX with variables and calculated columns
4. Reduce number of visuals per page
5. Use aggregations for large datasets
6. Implement row-level security efficiently
7. Remove unnecessary calculated columns
8. Use appropriate data types

### Q21: What is the difference between calculated columns and measures?
**Answer**:
- **Calculated Column**: Computed row-by-row at refresh, stored in table
- **Measure**: Computed at query time, not stored, aggregations

```dax
-- Calculated Column (per row)
Margin = sales[Revenue] - sales[Cost]

-- Measure (aggregation)
Total Margin = SUM(sales[Revenue]) - SUM(sales[Cost])
```

### Q22: How do you ensure dashboard security?
**Answer**:
1. Implement Row-Level Security (RLS)
2. Use role-based access control
3. Secure data sources with credentials
4. Set appropriate sharing permissions
5. Audit log monitoring
6. Regular security reviews

---

# ================================================================
# PART 3: STAKEHOLDER COMMUNICATION QUESTIONS
# ================================================================

### Q23: How do you explain a complex data finding to a non-technical stakeholder?
**Answer**:
1. Start with the business impact/conclusion
2. Use simple language, avoid jargon
3. Use analogies and real-world examples
4. Show visualizations, not just numbers
5. Connect to their goals/responsibilities
6. Provide actionable recommendations
7. Be prepared for follow-up questions

### Q24: How do you handle conflicting stakeholder requirements?
**Answer**:
1. Acknowledge all perspectives
2. Ask about priorities and trade-offs
3. Propose creative solutions if possible
4. Escalate to project sponsor if needed
5. Document decisions with rationale
6. Set clear expectations

### Q25: How do you manage stakeholder expectations on a BI project?
**Answer**:
1. Set realistic timelines and scope
2. Communicate progress regularly
3. Highlight dependencies early
4. Provide options/alternatives
5. Be transparent about challenges
6. Document changes formally

### Q26: How do you prioritize competing requests from stakeholders?
**Answer**:
1. Assess business impact
2. Consider data availability
3. Evaluate effort vs value
4. Factor in dependencies
5. Consult with leadership
6. Communicate prioritization rationale

### Q27: Describe a time you had to deliver bad news based on data
**Answer**:
(Sample answer)
"I discovered our top-performing product line was actually unprofitable when we factored in all costs. I prepared a clear presentation showing the full cost breakdown, alternative scenarios, and recommendations. By focusing on solutions rather than blame, we were able to pivot our strategy and recover the margin within 2 quarters."

### Q28: How do you ensure your dashboard provides actionable insights?
**Answer**:
1. Start with business questions, not data
2. Include "so what" context in tooltips
3. Add trend indicators and comparisons
4. Provide drill-down to root causes
5. Connect metrics to recommended actions
6. Get feedback from end users

---

# ================================================================
# PART 4: BUSINESS CASE STUDY QUESTIONS
# ================================================================

### Q29: Our monthly revenue dropped 30% compared to last month. How would you investigate?
**Answer**:
1. **Verify Data**: Check data completeness and quality
2. **Segment Analysis**: Break down by category, region, product, channel
3. **Compare Periods**: Day-by-day, week-by-week comparison
4. **Identify Patterns**: Date range, seasonality, holidays
5. **External Factors**: Market trends, competitor activity
6. **Internal Factors**: Marketing campaigns, website changes
7. **Statistical Significance**: Is the drop significant or normal variance?

```sql
-- Initial Investigation Query
SELECT 
    DATE(order_date) AS order_day,
    SUM(amount) AS daily_revenue,
    COUNT(*) AS order_count
FROM sales
WHERE order_date BETWEEN '2022-04-01' AND '2022-04-30'
GROUP BY DATE(order_date)
ORDER BY order_day;

-- Category Comparison
SELECT 
    category,
    SUM(amount) AS revenue,
    SUM(amount) * 100.0 / (SELECT SUM(amount) FROM sales) AS revenue_share
FROM sales
WHERE order_date BETWEEN '2022-04-01' AND '2022-04-30'
GROUP BY category
ORDER BY revenue_share DESC;
```

### Q30: How would you identify if a marketing campaign was successful?
**Answer**:
1. **Define Success Metrics**: Revenue, conversions, ROI, engagement
2. **Set Baseline**: Pre-campaign performance
3. **Control Group**: Compare against non-exposed customers
4. **Attribution**: First-touch, last-touch, multi-touch
5. **Statistical Analysis**: A/B testing, significance testing
6. **Cost-Benefit**: ROI calculation

### Q31: A product manager asks for a recommendation on which product to discontinue. How would you approach this?
**Answer**:
1. **Revenue Analysis**: Contribution to total revenue
2. **Margin Analysis**: Profit contribution after all costs
3. **Trend Analysis**: Declining or growing?
4. **Inventory Impact**: Carrying cost, turnover
5. **Cross-Sell Analysis**: Complementary product dependencies
6. **Customer Impact**: Churn risk from discontinuation
7. **Competitive Analysis**: Market position
8. **Recommendation**: Data-driven with scenario analysis

### Q32: How would you build a customer churn prediction model?
**Answer**:
1. **Define Churn**: What constitutes churn for our business?
2. **Data Collection**: Order history, engagement, demographics
3. **Feature Engineering**: RFM variables, behavioral patterns
4. **Model Selection**: Logistic regression, random forest, etc.
5. **Validation**: Train/test split, cross-validation
6. **Deployment**: Integrate into dashboard
7. **Monitoring**: Track prediction accuracy

### Q33: How do you determine the optimal price for a product?
**Answer**:
1. **Cost Analysis**: Floor price based on costs
2. **Competitive Analysis**: Market positioning
3. **Historical Analysis**: Price elasticity from past data
4. **Customer Segmentation**: WTP variation across segments
5. **A/B Testing**: Test price points
6. **Business Constraints**: Volume targets, margin requirements

---

# ================================================================
# PART 5: SCENARIO-BASED ANALYTICS QUESTIONS
# ================================================================

### Q34: Scenario: You have a dataset with 1 million rows. Queries are running very slow. How do you fix it?
**Answer**:
1. **Index Optimization**: Add appropriate indexes
2. **Query Optimization**: Avoid SELECT *, use WHERE clauses
3. **Database Design**: Normalize/denormalize as needed
4. **Hardware**: Check server resources
5. **Data Archival**: Move old data to archive tables
6. **Partitioning**: Partition large tables
7. **Materialized Views**: Pre-compute aggregations
8. **Caching**: Use query result caching

### Q35: Scenario: Your dashboard shows different numbers than a report from another team. How do you resolve?
**Answer**:
1. **Stay Calm**: Don't assume error on either side
2. **Data Source**: Compare underlying data sources
3. **Definitions**: Check if metric definitions match
4. **Filters**: Compare applied filters/date ranges
5. **Calculations**: Review formulas/logic
6. **Timing**: Check data refresh schedules
7. **Escalate if needed**: Bring both teams together
8. **Document**: Create shared metric definitions

### Q36: Scenario: A stakeholder asks for a new dashboard in 2 days. You have a backlog of items. What do you do?
**Answer**:
1. **Assess Urgency**: Understand the business need
2. **Quick Win Check**: Can this be done quickly with existing data?
3. **Prioritization Discussion**: Re-prioritize with manager
4. **Scope Management**: Offer MVP version
5. **Communicate**: Set expectations on backlog items
6. **Leverage Templates**: Use existing dashboard structure

### Q37: Scenario: You find a significant data quality issue in production data. What do you do?
**Answer**:
1. **Verify Issue**: Confirm the problem is real
2. **Assess Impact**: Who/what is affected?
3. **Communicate**: Alert stakeholders immediately
4. **Document**: Log the issue with details
5. **Root Cause**: Investigate why it happened
6. **Fix**: Implement data quality correction
7. **Prevent**: Add validation to prevent recurrence
8. **Monitor**: Set up quality checks

### Q38: Scenario: Leadership wants to cut your team's budget by 30%. How do you justify the value?
**Answer**:
1. **Quantify Impact**: ROI from data-driven decisions
2. **Efficiency Gains**: Hours saved on manual reporting
3. **Revenue Attribution**: Revenue influenced by analytics
4. **Cost Avoidance**: Problems prevented through insights
5. **Competitive Advantage**: Insights vs competitors
6. **Risk Mitigation**: Compliance, fraud detection
7. **Future Value**: Scalability for growth

### Q39: Scenario: Your model predicts something counterintuitive. How do you handle it?
**Answer**:
1. **Validate**: Check model accuracy and assumptions
2. **Data Check**: Verify data is correct
3. **Context**: Understand business context
4. **Deeper Dive**: Explore the surprising patterns
5. **Consult**: Discuss with domain experts
6. **Document**: Note the finding and follow-up
7. **Iterate**: Refine model if needed

### Q40: Scenario: A competitor just launched a similar dashboard. How do you stay ahead?
**Answer**:
1. **Competitive Analysis**: Understand their offering
2. **Unique Value**: Focus on what you do better
3. **Feedback Loop**: Gather user feedback
4. **Innovation**: Add new features/data sources
5. **Speed**: Respond quickly to needs
6. **Partnership**: Align with business strategy

---

# ================================================================
# PART 6: PYTHON & DATA CLEANING QUESTIONS
# ================================================================

### Q41: How do you handle missing values in a dataset?
**Answer**:
| Scenario | Method |
|---------|--------|
| Numeric, random missing | Mean/Median imputation |
| Numeric, non-random | Model-based imputation |
| Categorical | Mode or "Unknown" |
| Time series | Forward/back fill |
| High missing % | Drop column or rows |
| Intentional (e.g., cancelled) | Fill with 0 or specific value |

```python
# Common approaches
df['column'].fillna(df['column'].mean(), inplace=True)
df['column'].fillna(0, inplace=True)
df.dropna(thresh=0.8*len(df), inplace=True)  # Drop if 80% missing
```

### Q42: How do you detect and handle outliers?
**Answer**:
1. **Visual**: Box plots, scatter plots
2. **Statistical**: Z-scores, IQR method
3. **Domain Knowledge**: Business rules

```python
# IQR Method
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['amount'] < Q1-1.5*IQR) | (df['amount'] > Q3+1.5*IQR)]
```

### Q43: What is the difference between merge and concat in pandas?
**Answer**:
- **merge()**: SQL-style joins (INNER, LEFT, RIGHT, OUTER)
- **concat()**: Stack dataframes vertically or horizontally

### Q44: How do you optimize pandas operations for large datasets?
**Answer**:
1. Use appropriate dtypes (category vs object)
2. Use vectorized operations instead of loops
3. Use query() for filtering
4. Use chunking for large files
5. Consider using Polars or Dask for very large data
6. Use inplace operations carefully
7. Avoid copying data unnecessarily

### Q45: How do you handle duplicate records?
**Answer**:
```python
# Find duplicates
duplicates = df.duplicated(subset=['order_id'], keep=False)

# Remove duplicates
df_clean = df.drop_duplicates(subset=['order_id'], keep='first')

# Count duplicates
duplicate_count = df.duplicated(subset=['order_id']).sum()
```

---

# ================================================================
# PART 7: BEHAVIORAL QUESTIONS
# ================================================================

### Q46: Tell me about a time you had to learn a new technology quickly
**Answer**: (STAR format)
- **Situation**: Need to learn Power BI for executive dashboard
- **Task**: Complete dashboard in 2 weeks with no prior experience
- **Action**: Completed online training, built prototype, asked for feedback
- **Result**: Dashboard delivered on time, adopted by leadership

### Q47: Describe your most challenging analytics project
**Answer**: (Focus on methodology, problem-solving, impact)

"My most challenging project was analyzing customer churn for a subscription business. The data was fragmented across 5 systems, and definitions were inconsistent. I spent 3 weeks just understanding and cleaning the data. Once aligned, I identified 3 key churn predictors and built a prediction model that reduced churn by 15%."

### Q48: How do you stay updated with analytics trends?
**Answer**:
- Online courses (Coursera, Udemy)
- Blogs (Towards Data Science, Mode Analytics)
- Community events (Meetups, conferences)
- LinkedIn learning
- Kaggle competitions
- Industry publications

### Q49: Where do you see yourself in 5 years?
**Answer**: (Align with company's career path)
"Growing into a Senior BI role where I can lead analytics initiatives, mentor junior analysts, and influence strategic decisions. I see myself specializing in [area of interest] and becoming a go-to resource for data-driven insights."

### Q50: Why should we hire you for this role?
**Answer**: (Combine technical + soft skills + passion)

"I bring a unique combination of technical expertise and business acumen. My experience in end-to-end analytics - from data engineering to dashboard development to strategic recommendations - means I can deliver complete solutions. I'm passionate about turning data into actionable insights and have a track record of driving measurable business impact."

---

# ================================================================
# BONUS: LIVE SQL PRACTICE QUESTIONS
# ================================================================

### Practice Q1: Find the top 3 products by revenue for each month
```sql
WITH ranked_products AS (
    SELECT 
        MONTH(order_date) AS month,
        sku,
        SUM(amount) AS revenue,
        RANK() OVER (PARTITION BY MONTH(order_date) ORDER BY SUM(amount) DESC) AS rank
    FROM sales
    GROUP BY MONTH(order_date), sku
)
SELECT * FROM ranked_products WHERE rank <= 3;
```

### Practice Q2: Calculate 7-day rolling average of daily revenue
```sql
WITH daily_revenue AS (
    SELECT 
        order_date,
        SUM(amount) AS daily_rev
    FROM sales
    GROUP BY order_date
)
SELECT 
    order_date,
    daily_rev,
    AVG(daily_rev) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_7day
FROM daily_revenue;
```

### Practice Q3: Identify customers who have not purchased in 90 days
```sql
WITH customer_last_purchase AS (
    SELECT 
        city,
        MAX(order_date) AS last_purchase_date
    FROM sales
    GROUP BY city
)
SELECT 
    city,
    last_purchase_date,
    DATEDIFF(CURRENT_DATE, last_purchase_date) AS days_since_purchase
FROM customer_last_purchase
WHERE DATEDIFF(CURRENT_DATE, last_purchase_date) > 90;
```

### Practice Q4: Calculate month-over-month growth with comparison to same month last year
```sql
WITH monthly_metrics AS (
    SELECT 
        YEAR(order_date) AS year,
        MONTH(order_date) AS month,
        SUM(amount) AS revenue,
        COUNT(*) AS orders
    FROM sales
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT 
    m1.year,
    m1.month,
    m1.revenue AS current_revenue,
    m2.revenue AS prev_year_revenue,
    (m1.revenue - m2.revenue) / m2.revenue * 100 AS yoy_growth,
    m1.revenue - m3.revenue AS mom_growth,
    m3.revenue AS prev_month_revenue
FROM monthly_metrics m1
LEFT JOIN monthly_metrics m2 ON m1.month = m2.month AND m1.year = m2.year + 1
LEFT JOIN monthly_metrics m3 ON m1.year = m3.year AND m1.month = m3.month + 1
ORDER BY m1.year, m1.month;
```

---

# ================================================================
# ADDITIONAL RESOURCES
# ================================================================

## Recommended Reading
1. "Storytelling with Data" by Cole Nussbaumer Knafic
2. "The Data Warehouse Toolkit" by Ralph Kimball
3. "SQL Cookbook" by Anthony Molinaro
4. "Power BI Cookbook" by Brett Powell

## Online Resources
- [Microsoft Learn - Power BI](https://learn.microsoft.com/power-bi)
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/)
- [Kaggle - Python Tutorials](https://kaggle.com/learn)

## Practice Platforms
- [LeetCode - SQL](https://leetcode.com/problemset/database/)
- [HackerRank - SQL](https://www.hackerrank.com/domains/sql)
- [StrataScratch](https://platform.stratascratch.com/)

---

*Document prepared for interview preparation*
*Last Updated: [Current Date]*