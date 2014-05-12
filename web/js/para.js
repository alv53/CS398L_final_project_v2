function main(name){
  var margin = {top: 30, right: 10, bottom: 10, left: 30},
      width = 500 - margin.left - margin.right,
      height = 3000 - margin.top - margin.bottom;

  var x = d3.scale.linear()
      .range([0, width])

  var y = d3.scale.ordinal()
      .rangeBands([0, height]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .ticks(21)
      .orient("top");

  var tip = d3.tip()
  // #         color.write("<p style=\"color:#" + str(textColor)[2:] + "0000;\">")

      .html(function(d) { return "<div class=\"paragraph\"><span style=\"color:#00CD66\">" + d.pos + " positive : </span><span style=\"color:brown\">" + d.neg + " negative</span> sentences in paragraph " + d.para + "<br><br>Click to bar to full paragraph</p></div>"; })

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.call(tip);

  d3.tsv(name, type, function(error, data) {
    x.domain([-10,10])
    y.domain(data.map(function(d) { return d.para; }));

  svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar1")
      .attr("x", function (d) { return x(Math.min(0, d.pos)); })
      .attr("y", function (d) { return y(d.para); })
      .attr("width", function (d) { return Math.abs(x(d.pos) - x(0)); })
      .attr("height", y.rangeBand())
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)
      .on('click', function(d){
        document.location.href = "paragraphs/paragraph" + d.para + ".html";
      });


  svg.selectAll(".bar2")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar2")
      .attr("x", function (d) { return x(Math.min(0, -d.neg)); })
      .attr("y", function (d) { return y(d.para); })
      .attr("width", function (d) { return Math.abs(x(-d.neg) - x(0)); })
      .attr("height", y.rangeBand())
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)
      .on('click', function(d){
        document.location.href = "paragraphs/paragraph" + d.para + ".html";
      });



  svg.append("g")
      .attr("class", "x axis")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
    .append("line")
      .attr("x1", x(0))
      .attr("x2", x(0))
      .attr("y2", height);

  });
  function type(d) {
    d.value = +d.value;
    return d;
  }
}
