data = Plotly.d3.csv("C:\Users\micha\Project-2-Job_Costing_App\plotly\project_details.csv").then(
let xField = 'months',
let yField = 'est_labor_expense')

let selectorOptions = {
    buttons: [{
        step: 'month',
        stepmode: 'backward',
        count: 1,
        label: '1m'
    }, {
        step: 'month',
        stepmode: 'backward',
        count: 6,
        label: '6m'
    }, {
        step: 'year',
        stepmode: 'todate',
        count: 1,
        label: 'YTD'
    }, {
        step: 'year',
        stepmode: 'backward',
        count: 1,
        label: '1y'
    }, {
        step: 'all',
    }],
};

Plotly.d3.csv(data, function(err, rawData) {
    if(err) throw err;

    let data = prepData(rawData);
    let layout = {
        title: 'Estimated Labor Expense vs Acutual Labor',
        xaxis: {
            rangeselector: selectorOptions,
            rangeslider: {}
        },
        yaxis: {
            fixedrange: true
        }
    };

    Plotly.newPlot('../plotly/app2.js', data, layout);
});

function prepData(rawData) {
    let x = [];
    let y = [];

    rawData.forEach(function(datum, i) {

        x.push(new Date(datum[xField]));
        y.push(datum[yField]);
    });

    return [{
        mode: 'bar',
        x: x,
        y: y
    }];
}