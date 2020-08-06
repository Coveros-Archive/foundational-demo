stage("test") {
    node {
        println "Hello world"
        Date date = new Date()
        def timestamp = date.getTime()
        // URL url = new URL()
        // HttpURLConnection connection = (HttpURLConnection) url.openConnection()
        def api_base = "https://coveros.spiraservice.net/services/v5_0/RestService.svc"
        def data = """\
            "ArtifactTypeId":1,
            "ConcurrencyDate":"/Date(${timestamp})/",
            "ExecutionStatusId":2,
            "StartDate":"/Date(${timestamp})/",
            "TestCaseId":35,
            "TestRunTypeId":1,
            "TestRunFormatId":0,
            "RunnerName":"jenkins",
            "AutomationHostId": 7,
            "RunnerStackTrace": "Foo",
            "RunnerTestName": "Bar",
            "RunnerMessage": "spam"}
        """
        def connection = new URL("${api_base}/projects/10/test-runs/record").openConnection()
        connection.setRequestMethod("POST")
        connection.setDoOutput(true)
        connection.setRequestProperty("Content-Type", "application/json")
        connection.getOutputStream().write(data.getBytes("UTF-8"))
        def post = connection.getResponseCode()
        println post
        println post.getInputStream.getTest()

        if (post == 200) {
            println post.getInputStream().getText()
        }
    }
} 