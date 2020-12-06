$('#dashboard_search').on('keyup', function(){
    let value = $(this).val()
    console.log('Value:', value)
    let data = searchTable(value, project_list)
    buildTable(data)
})

buildTable(project_list)

function searchTable(value, data){
    let filteredData = []

    for (var i = 0; i < data.length; i++){
        value = value.toLowerCase()
        let name = data[i].name.toLowerCase()

        if (name.includes(value)){
            filteredData.push(data[i])
        }
    }

    return filteredData
}

function buildTable(data){
    let table = document.getElementById('dashboardTable')

    table.innerHTML = ''

    for (var i = 0; i < data.length; i++){
        var row = `<tr>
                        <td>${data[i].name}</td>
                        <td>${data[i].revenue}</td>
                        <td>${data[i].est_labor_hours}</td>
                        <td>${data[i].est_labor_hours}</td>
                        <td>${data[i].est_labor_expense}</td>
                        <td>${data[i].est_labor_expense}</td>
                        <td>${data[i].act_start_date}</td>
                   </tr>`
        
        table.innerHTML += row
    }
}

