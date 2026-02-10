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

# Count of each product
productcounts <- df %>%
  count(`Product Name`, sort = TRUE)
print(productcounts)


