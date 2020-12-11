Plotly.d3.csv("..//static/result.json").then({
  x: "est_labor_expense",
  y: "act_start_date",
}),
  {
    sliders: [
      {
        pad: { t: 30 },
        len: 0.5,
        x: 0.5,
        currentvalue: {
          xanchor: "right",
          prefix: "color:",
          font: {
            color: "green",
            size: 20,
          },
        },
        transition: { duration: 500 },
        steps: [
          {
            label: "red",
            method: "animate",
            args: [
              ["red"],
              {
                mode: "immediate",
                frame: { redraw: false, duration: 500 },
                transition: { duration: 500 },
              },
            ],
          },
          {
            label: "green",
            method: "animate",
            args: [
              ["green"],
              {
                mode: "immediate",
                frame: { redraw: false, duration: 500 },
                transition: { duration: 500 },
              },
            ],
          },
          {
            label: "blue",
            method: "animate",
            args: [
              ["blue"],
              {
                mode: "immediate",
                frame: { redraw: false, duration: 500 },
                transition: { duration: 500 },
              },
            ],
          },
        ],
      },
    ],
    updatemenus: [
      {
        type: "buttons",
        showactive: false,
        x: 0.05,
        y: 0,
        xanchor: "right",
        yanchor: "top",
        pad: { t: 60, r: 20 },
        buttons: [
          {
            label: "Play",
            method: "animate",
            args: [
              null,
              {
                fromcurrent: true,
                frame: { redraw: false, duration: 1000 },
                transition: { duration: 500 },
              },
            ],
          },
        ],
      },
    ],
  },
  frames;
[
  {
    name: "January",
    data: [
      {
        y: [2, 1, 3],
        "line.color": "red",
      },
    ],
  },
  {
    name: "February",
    data: [
      {
        y: [3, 2, 1],
        "line.color": "orange",
      },
    ],
  },
  {
    name: "March",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "yellow",
      },
    ],
  },
  {
    name: "April",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "green",
      },
    ],
  },
  {
    name: "May",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "blue",
      },
    ],
  },
  {
    name: "June",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "purple",
      },
    ],
  },
  {
    name: "July",
    data: [
      {
        y: [2, 1, 3],
        "line.color": "brown",
      },
    ],
  },
  {
    name: "August",
    data: [
      {
        y: [3, 2, 1],
        "line.color": "magenta",
      },
    ],
  },
  {
    name: "September",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "tan",
      },
    ],
  },
  {
    name: "October",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "cyan",
      },
    ],
  },
  {
    name: "November",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "olive",
      },
    ],
  },
  {
    name: "December",
    data: [
      {
        y: [1, 3, 2],
        "line.color": "maroon",
      },
    ],
  },
];
