console.log("Hello")
d3.json("/").then(
    data=> {
        console.log(data)
    }
)