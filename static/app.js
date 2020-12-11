// Search Table
$("#dashboard_search").on("keyup", function () {
  let value = $(this).val();
  console.log("Value:", value);
  let data = searchTable(value, project_list);
  buildTable(data);
});



function searchTable(value, data) {
  let filteredData = [];

  for (const item in data) {
    value = value.toLowerCase();
    let name = data[item].project_name.toLowerCase();

    if (name.includes(value)) {
      filteredData.push(data[item]);
    }
  }

  return filteredData;
}
// Sort Table
$('th').on('click', function(){
  let column = $(this).data('column')
  let order = $(this).data('order')
  let arrow = $(this).html()
  arrow = arrow.substring(0, arrow.length - 1)


  if(order == 'desc'){
    $(this).data('order', "asc")
    desc_project_list = project_list.sort((a,b) => a[column] > b[column] ? 1 :
    -1)
    arrow += '&#9660'
  }else{
    $(this).data('order', "desc")
    asc_project_list = project_list.sort((a,b) => a[column] < b[column] ? 1 :
    -1)
    arrow += '&#9650'
  }
  $(this).html(arrow)
  buildTable(project_list)
})


buildTable(project_list);

function buildTable(data) {
  let table = document.getElementById("dashboardTable");

  table.innerHTML = "";

  for (const item in data) {
    var row = `<tr>
                        <td>${data[item].project_name}</td>
                        <td>${data[item].fin_act_revenue}</td>
                        <td>${data[item].fin_est_labor_hours}</td>
                        <td>${data[item].fin_act_labor_hours}</td>
                        <td>${data[item].fin_est_labor_expense}</td>
                        <td>${data[item].fin_act_labor_expense}</td>
                        <td>${data[item].act_start_date}</td>
                   </tr>`;

    table.innerHTML += row;
  }
}
for (const item in project_list) {
    // console.log(item)
  console.log(project_list[item])
}

// function optionChange(value) {
//   for(const item in project_list) {
//       console.log(item)
      // console.log(project_list[item])
      
      
    // }
// }
