Feature: Search for a company

    Search feature should allow users to search for a company by name or stock symbol. 

    Scenario: Search for a company that is in the database by name
        Given I am on the home page
        When I search for "Alphabet"
        Then I should see a loading spinner
        Then I should see a card with the prediction for "Alphabet"
        And The card should say either buy or sell
        And The card should have text
        * The text should include the company name, "Alphabet"
        * The text should include the company stock symbol, "GOOG"
        * The text should include the prediction, "buy" or "sell", in natural language
        * The text should include the probability of the stock price going up or down
        * The text should include the financial information for the company that supports the prediction
        * The text should include the financial information for the company that goes against the prediction
        * The text should include a disclaimer so we don't get sued

    Scenario: Search for a company that is in the database by stock symbol
        Given I am on the home page
        When I search for "GOOG"
        Then I should see a loading spinner
        Then I should see a card with the prediction for "Alphabet"
        And The card should say either buy or sell
        And The card should have text
        * The text should include the company name, "Alphabet"
        * The text should include the company stock symbol, "GOOG"
        * The text should include the prediction, "buy" or "sell", in natural language
        * The text should include the probability of the stock price going up or down
        * The text should include the financial information for the company that supports the prediction
        * The text should include the financial information for the company that goes against the prediction
        * The text should include a disclaimer so we don't get sued

    Scenario: Search for a company that is not in the database
        Given I am on the home page
        When I search for "ASML"
        Then I should see a loading spinner
        Then I should see a card informing me that data for "ASML" could not be found