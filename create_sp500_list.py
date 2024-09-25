import sp500_list_getter

sp500 = sp500_list_getter.Get_sp500_list()
sp500.request_to_pd()
sp500.get_earnings_date()
sp500_df = sp500.get_df()
sp500_df.to_csv('data.csv', sep=',', index=False)
print(sp500_df)


"""
notera denna py filen har bara användts för att webscrapa alla företag in sp500 som sedan skall passeras till databasen.
dataframen sparas till en csv fil som man senare kan använda.

denna filen används ej i den schema lagda updateringen 
och då gör vi då inga tester eller kör denna filen igen samt igen docstring/kommentarer.
Men kolla gärna igenom denna och python modulen sp500_list_getter.
"""