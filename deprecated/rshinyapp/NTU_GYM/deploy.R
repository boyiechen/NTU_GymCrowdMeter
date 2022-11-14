# Deploy
library(rsconnect)
rsconnect::setAccountInfo(name='andyfish',
                          token='B349288EFFDA7D7540B7235199BA5A34',
                          secret='tWnfXaXgOTkYdyAz1YUVRIz4rv8TLmvlasPpHDbu')

rsconnect::deployApp('/Users/Andy 1/google_drive/Coding_Projects/NTU_GYM_counter/shinyapp/NTU_GYM')
