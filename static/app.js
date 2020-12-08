// Search Table
$("#dashboard_search").on("keyup", function () {
  let value = $(this).val();
  console.log("Value:", value);
  let data = searchTable(value, project_list);
  buildTable(data);
});



function searchTable(value, data) {
  let filteredData = [];

  for (var i = 0; i < data.length; i++) {
    value = value.toLowerCase();
    let name = data[i].name.toLowerCase();

    if (name.includes(value)) {
      filteredData.push(data[i]);
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

  for (var i = 0; i < data.length; i++) {
    var row = `<tr>
                        <td>${data[i].name}</td>
                        <td>${data[i].revenue}</td>
                        <td>${data[i].est_labor_hours}</td>
                        <td>${data[i].est_labor_hours}</td>
                        <td>${data[i].est_labor_expense}</td>
                        <td>${data[i].est_labor_expense}</td>
                        <td>${data[i].act_start_date}</td>
                   </tr>`;

    table.innerHTML += row;
  }
}
