import pandas as pd
from .preprocess import Preprocess
class Duplicates(object):
    
    def __init__(self):
        pass
    
    def drop_duplicates(self,df):
        
        #dropping duplicate methods
        self.drop_duplicate_rows(df)
        self.drop_duplicate_columns(df)
        
    def drop_duplicate_rows(self,df):
        """Drops duplicate rows"""
        dups = df.shape[0]-df.drop_duplicates().shape[0]
        print('Duplicate rows detected: ', dups)
        if dups!=0:

            #user-input
            opt = input('Drop Duplicate rows (Please type yes or no): ')
            if opt == 'no':
                return
            elif opt=="yes":
                df.drop_duplicates(inplace=True)
                print('Rows removed: ',dups)
            else:
                print("Please enter yes or no only ")
                self.drop_duplicate_rows(df)
                
    def drop_duplicate_columns(self,df):
        """Drops duplicate columns or renames them."""
        duplicate_columns = df.columns.values[df.columns.duplicated()]
        print('Columns with duplicate names')
        print(duplicate_columns)
        #one problem here is that columns with duplicate names are not processed so I need to process them after dropping them
        #or renaming them.
        if duplicate_columns:
            display(df[duplicate_columns])

        if len(duplicate_columns)==0:
            return
        #user input
        opt = input('Drop columns with duplicate names(Please type yes or no): ')
        
        if opt=='no':
            opt = input('Rename Duplicate columns(Please type yes or no): ')
            if opt=='no':
                return 
            elif opt=="yes":
                to_be_processed = []
                final_columns = df.columns.values
                for column in duplicate_columns:
                    nos = 0
                    for i in range(len(final_columns)):
                        if final_columns[i] == column:
                            final_columns[i]  = column+str(nos)
                            to_be_processed.append(column+str(nos))
                            nos+=1
                    if nos!=0:
                        print(column,' has be converted to ',[column+str(i) for i in range(nos)])
                df.columns = final_columns
                Preprocess().preprocess(df,columns = to_be_processed)
                return
            else:
                print("Please enter yes or no only")
                self.drop_duplicate_columns(df)

        elif opt=="yes":
            print('Warning: Columns Dropped ',duplicate_columns)
            for column in duplicate_columns:
                temp  = pd.Series(df[column].iloc[:,0])
                df.drop(columns = [column],axis=1,inplace = True)
                df[column] = temp
            Preprocess().preprocess(df,columns=duplicate_columns)
        else:
            print("Please Enter yes or no only")
            self.drop_duplicate_columns(df)
