library(shiny)
library(reticulate)
library('shinydashboard')
library(shinyWidgets)
library(dplyr)
library(ggplot2)
library(plotrix)
ui <- fluidPage(
  setBackgroundColor("#d9d9d9"),
  tags$script(src="https://kit.fontawesome.com/66aa7c98b3.js",crossorigin="anonymous"),
  tags$style(HTML("
    
    ul.nav.nav-tabs li {
        background-color: black !important;
    }     
    .tabbable {
       margin-bottom: 50px;
    }
    .tabbable > .nav > li[class=active] > a {
           background-color: black;
           color: #fcc;
           border: #000;
    }
    #barplot {
      margin-top: 45px;
    }
    #text1, #PredictedRating, #MaxAndMinRating {
      margin-top: 45px;
      font-size: 35px;
    }
    
        
    .footer{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #263238;
        text-align: center;
        color: #f4f4f4;
    }
    
    .icons{
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    .icons a{
        text-decoration: none;
        font-size: 2rem;
        margin: 0rem;
        color: #f4f4f4;
    }
    
    
    @media (max-width: 500px){
        html{
            font-size: 50%;
        }
    }    
    
    @media(min-width: 501px) and (max-width: 768px){
        html{
        font-size: 50%;
        }
    }    
  ")),
  tags$h1("Analyze CF",style="text-align:center;")
  ,fluidRow(column(3,textInput(inputId="val",label="Enter your codeforces handle",placeholder = "eg. tourist")),column(4,actionButton(inputId = "click",label="enter",style = "margin-top:25px;background-color: #bfbbbb"))),
  tabsetPanel(tabPanel("Home",HTML('<center><img src="LOGO.gif"></center>')),
              tabPanel("Hacking",tags$h1("Top 5 hackers",style="text-align:center"),dataTableOutput(outputId = "hackfreq"),plotOutput(outputId = "pie")),
              tabPanel("Rating",tags$h2("Rating Distribution of the user"), plotOutput(outputId = "Ratingplot"), textOutput(outputId = "MaxAndMinRating"), textOutput(outputId = "PredictedRating")),
              tabPanel("problems",plotOutput(outputId = "barplot"),textOutput(outputId = "text1")),
              tabPanel("Blogs", tags$h2("Blog details of the corresponding user"), dataTableOutput(outputId = "BlogDetails"), actionButton(inputId = "Piechart",label="Pie chart",style = "margin-top:25px"), plotOutput(outputId = "piechart"), tags$h2("Ratingwise distribution of blogs"), plotOutput(outputId = "RatingBarplot"))
              ),
  tags$footer(class="footer",tags$div(class="icons",tags$a(href="https://github.com/VaibhaveS/AnalyzeCF",tags$i(class="fab fa-github")),tags$p(class="company-name","")))
)


server <- function(input, output) {
  
  submission_data <- eventReactive(input$click,{
    SubmissionData%>%filter(Handle==input$val)%>%select(c(3:5))
  })
  
  problems_data <- eventReactive(input$click,{
    probsData%>%filter(Handle==input$val)%>%dplyr::select(-c(1))
  })
  
  most_hacks <- eventReactive(input$click,{
    as.data.frame(table(HackData%>%filter(Verdict=='HACK_SUCCESSFUL',defender==input$val)%>%select("Hacker")))
    
  })
  ratingData <- eventReactive(input$click, {as.data.frame(RatingData %>% filter(User == input$val))})
  ratingPredictionData <- eventReactive(input$click, {as.data.frame(filter(RatingPredictionData, User == input$val))})
  blogidData <- eventReactive(input$click,{as.data.frame(blogIdData %>% filter(Author == input$val))})
  commentData <- eventReactive(input$Piechart,{as.data.frame(blogIdData %>% filter(Author == input$val))})
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
  
  output$piechart <- renderPlot({
    commentGreater50 <- commentData() %>% filter(No_of_comments >= 50)
    commentLess50 <- commentData() %>% filter(No_of_comments < 50)
    label <- c("No of comments >= 50","No of comments < 50")
    x <- nrow(commentGreater50)
    y <- nrow(commentLess50)
    data <- c(x,y)
    print(data)
    piepercent<- round(100 * data/nrow(commentData()), 1)
    pie(data,labels=piepercent,col=rainbow(length(data)),main="blog comments distribution")
    legend("topright",label,cex=0.8,fill=rainbow(length(data)))
  })
  output$text1 <- renderText({
    z=c()
    for (i in names(problems_data())){
      z <- c(z,problems_data()[, i])
    }
    best <- data.frame(tag = names(problems_data()),rating=z)
    View(best)
    newdata <- arrange(best,rating)
    View(newdata)
    string = "The least practiced categories are - "
    
    for(i in 1:5) {
      string=paste(string,paste(toString(i),") "));
      string=paste(string,newdata[i,"tag"],sep=" ")
    }
    string
  })
  output$barplot <- renderPlot({
    z=c()
    for (i in names(problems_data())){
      z <- c(z,problems_data()[, i])
    }
    best <- data.frame(tag = names(problems_data()),rating=z)
    ggplot(data=best, aes(x=tag, y=rating)) +
      geom_bar(stat="identity")+  ggtitle("distribution of problem ratings by tags") +
      theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5),plot.title = element_text(hjust = 0.5))
  })
  output$BlogDetails <- renderDataTable({blogidData()}, options = list(info = FALSE, searching = FALSE))
  output$RatingBarplot <- renderPlot({ggplot(blogData, aes(Rating, BlogCount)) + geom_bar(stat = "identity", width = 100) + theme(axis.text = element_text(size=12, colour =  'black'))})
  output$Ratingplot <- renderPlot({ggplot(ratingData(), aes(x = Rating)) + geom_density()})
  output$MaxAndMinRating <- renderText(paste("Maximum rating of the user is", max(ratingData()$Rating), " and the minimum rating is ", min(ratingData()$Rating), sep = " "))
  output$PredictedRating <- renderText({
    model <- loess(RatingPredictionData$CurrRating ~ RatingPredictionData$CurrRating + RatingPredictionData$AvgRatingChange, data = RatingPredictionData)
    res <- model %>% predict(ratingPredictionData())
    usr <- RatingPredictionData$User
    ind <- which(usr == input$val)
    print(paste("The Predicted Rating of the user is: ", floor(res[ind])))
  })
}
HackData <- read.csv("Hacks.csv")
SubmissionData <- read.csv("Submissions.csv")
blogIdData <- read.csv("BlogId.csv")
blogData <- read.csv("Blogs.csv")
probsData <- read.csv("problems.csv")
RatingData <- read.csv("Rating.csv")
RatingPredictionData <- read.csv("Rating_Prediction.csv")

View(probsData)
shinyApp(ui, server)