Feature: Company ranking

    Page ranking all companies predictions have been made for.

    Scenario: Go to rankings page from home page
        Given I am on the home page
        And I have searched for companies that returned results, for example:
            | Company Name |
            | Apple        |
            | Google       |
            | Microsoft    |
            | Meta         |
        When I click the "Top Recomendations" link
        Then I should be on the rankings page
        And I should see the "Top Recomendations" header
        * I should see a table with the following columns:
            | Company Name | Recomendation | Probability of price increase | Prediction Date |
        * I should the companies I have searched for in the table
        * I should see the companies in order of probability of price increase (descending)

    Scenario: Get prediction explanation from company rankings page
        Given I am on the "Top Recomendations" page
        When I click the expander on a company in the table
        Then I should see the explanation for the prediction that was generated when that prediction was made