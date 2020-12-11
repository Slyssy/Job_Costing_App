console.log("HelloWorld")

console.log(project_dict)

let keys = Object.keys(project_dict)
console.log(keys)

let values = Object.values(project_dict)
console.log(values)

// let estx = [keys[7]];
// console.log(estx)
// let actx = [keys[13]]
// console.log(actx)
// let esty = [values[7]];
// console.log(esty)
// let acty = [values[13]]
// console.log(acty)


let trace1 ={
    x: ["Bdg. Labor Exp."],
    y: [values[7]],
    name: "Budgeted Labor Expense",
    type: 'bar',
    marker: {
        color: 'rgb(219, 217, 217)',
        opacity: 0.5
    }
};

let trace2 ={
    x: ["Act. Labor Exp."],
    y: [values[13]],
    name: "Actual Labor Expense",
    type: 'bar',
    marker: {
        color: 'rgb(235, 40, 40)',
        opacity: 0.5
    }
};

let expData = [trace1, trace2];

let expLayout = {
    title: "Estimated vs. Actual Labor Expense",
    barmode: 'group',
    yaxis: {
        title: "Labor Expense ($)"
    }
};

Plotly.newPlot('eva_exp_bar', expData, expLayout);

let trace3 ={
    x: ["Bdg. Labor Hours"],
    y: [values[5]],
    name: "Budgeted Labor Hours",
    type: 'bar',
    marker: {
        color: 'rgb(219, 217, 217)',
        opacity: 0.5
    }
};

let trace4 ={
    x: ["Act. Labor Hours     "],
    y: [values[11]],
    name: "Actual Labor Hours",
    type: 'bar',
    marker: {
        color: 'rgb(235, 40, 40)',
        opacity: 0.5
    }
};

let hourData = [trace3, trace4];

let hourLayout = {
    title: "Estimated vs. Actual Labor Hours",
    barmode: 'group',
    yaxis: {
    title: "Labor Hours"
    }
};

Plotly.newPlot('eva_hr_bar', hourData, hourLayout);