// Select Employee Name
var employees = dropdown_dict.employee_list.map((d) => d.name);
var ele = document.getElementById("name");
for (var i = 0; i < employees.length; i++) {
  var opt = employees[i];

  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;

  ele.add(el);
}

// Select Project Name
var projects = dropdown_dict.project_list.map((d) => d.name);
var ele = document.getElementById("proName");
for (var i = 0; i < projects.length; i++) {
  var opt = projects[i];
  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;
  ele.add(el);
}
