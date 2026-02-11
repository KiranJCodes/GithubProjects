# R approach (tidyverse)

library(tidyverse)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

df <- read_csv("ECOMM_Sales_Data.csv")


summary(df)

## orders are from 2022 -> 2024
## all data is cleaned and prepared. 



# Quick analysis
df %>%
  filter(Sales > 0) %>%
  group_by(Category, Region) %>%
  summarise(Total = sum(Sales)) %>%
  ggplot(aes(Category, Total, fill = Region)) + 
  geom_col()


# 1 Most profitable month

df <- df %>%
  mutate(month = format(`Order Date`, "%m"))

PFM <- df %>% 
  group_by(month) %>%
  summarise(total_sum = sum(Profit)) %>%
  arrange(desc(total_sum))


top <- head(PFM,3)
bot <- tail(PFM,3)

combined <- bind_rows(
  top %>% mutate(type = "Top 3"),
  bot %>% mutate(type = "Bottom 3")
)

ggplot(combined, aes(x = reorder(month, -total_sum), y = total_sum, fill = type)) +
  geom_col() +
  scale_fill_manual(values = c("Top 3" = "darkgreen", "Bottom 3" = "darkred")) +
  labs(title = "Top vs Bottom Profitable Months", x = "Month", y = "Total Profit") +
  theme_minimal() +
  facet_wrap(~type, scales = "free_x")

 # 1a

MS <- df %>%
  group_by(month, `Product Name`) %>%
  summarise(totalSold = sum(Quantity, na.rm = TRUE)) %>%
  arrange(desc(totalSold))

MStop <- MS %>%
  group_by(month) %>%
  slice_max(totalSold, n = 1) %>%
  arrange(desc(totalSold))

print(MStop)

ggplot(MStop, aes(x = month, y = totalSold, fill = `Product Name`)) +
  geom_col() +
  geom_text(aes(label = `Product Name`), angle = 90, hjust = 1.1, size = 3, color = "white") +
  labs(title = "Most Sold Product Each Month", x = "Month", y = "Quantity") +
  theme_minimal()


# 2 Unique product names

# All unique product names
unique_products <- unique(df$`Product Name`)
print(unique_products)

#  2a Count of each product
productcounts <- df %>%
  count(`Product Name`, sort = TRUE)
print(productcounts)


#  2b Most Profitable products
ProfitSum <- df %>%
  group_by(`Product Name`) %>%
  summarise(MP = sum(Profit, na.rm = TRUE)) %>%
  arrange(desc(MP))

ggplot(ProfitSum, aes(x = `Product Name`, y = MP)) + 
  geom_col(fill = 'black') + 
  geom_text(aes(label = `Product Name`), angle = 90, hjust = 1.1, size = 3, color = 'yellow') +
  labs(title = "Most Profitable Products", x = 'Name', y = 'Sales') +
  theme_minimal()

# 3 Different product categories

ggplot(df, aes(x = Category, y = Sales, fill = Category)) +
  geom_boxplot() +
  labs(title = "Profit Distribution by Sales")

# 3a most sold category in each region
Region <- df %>%
  group_by(`Region`,`Category`) %>%
  summarise(RegSale = sum(Sales,na.rm = TRUE)) %>%
  arrange(Region)

topcat <- Region %>%
  group_by(Region) %>%
  slice_max(RegSale, n = 1)

print(topcat)


# 4 find average order quantity

ggplot(df, aes(x = Quantity)) +
  geom_density(fill = "steelblue", alpha = 0.6) +
  labs(title = "Density of Order Quantities", x = "Quantity", y = "Density") +
  theme_minimal()


# 5 most sold product of  all time

AlltimeSold <- df %>%
  group_by(`Product Name`) %>%
  summarise(ATS = sum(Quantity, na.rm = TRUE)) %>%
  arrange(desc(ATS))

print(head(AlltimeSold,3))

# 5a its % of sales 
AlltimeSold <- AlltimeSold %>%
  mutate(sales_pct = ATS / sum(ATS) * 100)


# 5b Its % of profit

product_profit <- df %>%
  group_by(`Product Name`) %>%
  summarise(total_profit = sum(Profit, na.rm = TRUE))


AlltimeSold <- AlltimeSold %>%
  left_join(product_profit, by = "Product Name") %>%
  mutate(profit_pct = total_profit / sum(total_profit, na.rm = TRUE) * 100)

print(head(AlltimeSold, 5))



# 6 profit Category by Region and Month

df %>% 
  group_by(Category, Region) %>% 
  summarise(profit = sum(Profit)) %>% 
  ggplot(aes(Category, Region, fill = profit)) + 
  geom_tile()

# 6a profit Product by Region and Month

df %>% 
  group_by(`Product Name`, Region) %>% 
  summarise(profit = sum(Profit)) %>% 
  ggplot(aes(`Product Name`, Region, fill = profit)) + 
  geom_tile()
