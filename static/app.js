console.log("Hello")

buildTable(project_list)

function buildTable(data){
    let table = document.getElementById('#dashboardTable')

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