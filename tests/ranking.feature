Feature: Company ranking

    Table ranking all companies predictions have been made for.

    Scenario: See rankings table from home page
        Given I am on the home page
        Then I should see the "Top Recomendations" header
        And I should see a table with the following columns:
            | Company Name | Recomendation | Probability of price increase | Prediction Date |
        * I should see the five companies I have searched for that have the highest probability of stock price increase in the table
        * I should see the companies in order of probability of price increase (descending)

    Scenario: Go to rankings page from home page
        Given I am on the home page
        And I have searched for companies that returned results, for example:
            | Company Name |
            | Apple        |
            | Google       |
            | Microsoft    |
            | Meta         |
        When I click the "Top Recomendations" link (top right) or the "Click to see more" link (bottom of the table)
        Then I should be on the rankings page
        And I should see the "Top Recomendations" header
        * I should see a table with the following columns:
            | Company Name | Recomendation | Probability of price increase | Prediction Date |
        * I should see all the companies I have searched for in the table
        * I should see the companies in order of probability of price increase (descending)

    Scenario: Get prediction explanation from company rankings table
        Given I am on the rankings page or the home page
        When I click the expander on a company in the table
        Then I should see the explanation for the prediction that was generated when that prediction was made