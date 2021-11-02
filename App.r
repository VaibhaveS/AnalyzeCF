library(shiny)
library(reticulate)
library(dplyr)

ui <- fluidPage(
  tags$h1("Analyze CF",style="text-align:center")
  ,fluidRow(column(3,textInput(inputId="val",label="Enter your codeforces handle")),column(4,actionButton(inputId = "click",label="enter",style = "margin-top:25px"))),
  tabsetPanel(tabPanel("Home",HTML('<center><img src="LOGO.gif"></center>')),tabPanel("Hacking",tags$h1("Top 5 hackers",style="text-align:center")
               ,dataTableOutput(outputId = "hackfreq"),plotOutput(outputId = "pie")),
               tabPanel("Rating"),tabPanel("Blogs"))
)


server <- function(input, output) {

  submission_data <- eventReactive(input$click,{
    SubmissionData%>%filter(Handle==input$val)%>%select(c(3:5))
  })
  
  most_hacks <- eventReactive(input$click,{
    as.data.frame(table(HackData%>%filter(Verdict=='HACK_SUCCESSFUL',defender==input$val)%>%select("Hacker")))
    
  })
  
  output$hackfreq <- renderDataTable({most_hacks()},
                                     options = list(searching = FALSE,filter="top", selection="multiple", escape=FALSE,info=FALSE,lengthChange=FALSE,columns=list(list(title="Hacked by"),list(title="Frequency"))))

  output$pie <- renderPlot({
    label <- c("Accepted","Hacked","Others (WA,TLE,RE)")
    x <- as.integer(submission_data()["Accepted"])
    y <- as.integer(submission_data()["Hacked"])
    z <- as.integer(submission_data()["Other"])
    data <- c(x,y,z)
    print(data)
    piepercent<- round(100*data/sum(data), 1)
    pie(data,labels=piepercent,col=rainbow(length(data)),main="Submissions pie chart")
    legend("topright",label,cex=0.8,fill=rainbow(length(data)))
  })
  
  
}

HackData <- read.csv("C:/Users/HP/Desktop/CP_FDA/AnalyzeCF/Hacks.csv")
SubmissionData <- read.csv("C:/Users/HP/Desktop/CP_FDA/AnalyzeCF/Submissions.csv")
shinyApp(ui, server)

