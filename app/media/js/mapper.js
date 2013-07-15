function plotMap(){
	var links = [
	  {source: "Electric Consumption by ZIP Code - 2010", target: "Electricity Use Normalised by Household"},
	  {source: "2010 Census - Population", target: "Electricity Use Normalised by Household"},
	  {source: "2010 Census - Households", target: "Electricity Use Normalised by Household"},
	  {source: "NYC Zipcode JSON", target: "Electricity Use Normalised by Household"},
	  {source: "NYC Zipcode JSON", target: "VisioNYC"},
	  {source: "NYC Zipcode JSON", target: "Mapping the Spread of the West Nile Virus"},
	  {source: "NYC Zipcode Shapefile", target: "NYC Zipcode JSON"},
	  {source: "Retail Sales of Electricity - Monthly", target: "Electricity Use Normalised by Household"},
	  {source: "Raw Con Ed Electricity Data", target: "Electric Consumption by ZIP Code - 2010"},
	];
	
	var licenses={"Electric Consumption by ZIP Code - 2010":"Data Commons",
				  "Electricity Use Normalised by Household":"CC-BY-NC-SA",
				  "2010 Census - Population":"Data Commons",
				  "2010 Census - Households":"Data Commons",
				  "NYC Zipcode Shapefile":"Open Data Commons Open Database License (ODbL)",
				  "NYC Zipcode JSON":"Open Data Commons Open Database License (ODbL)",
				  "VisioNYC":"Unknown",
				  "Mapping the Spread of the West Nile Virus":"Unknown",
				  "Retail Sales of Electricity - Monthly":"Data Commons",
				  "Raw Con Ed Electricity Data":"Open Data"
				  };
	
	var colours={"Data Commons":"green","Open Data":"lightgreen","CC-BY-NC-SA":"blue","Open Data Commons Open Database License (ODbL)":"yellow","Unknown":"grey"};
	
	var nodes = {};
	
	// Compute the distinct nodes from the links.
	links.forEach(function(link) {
	  link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
	  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
	});
	
	//var w = 960,
	//    h = 700;
	var w = window.innerWidth*15/24.,
	    h = window.innerHeight;
	
	var force = d3.layout.force()
	    .nodes(d3.values(nodes))
	    .links(links)
	    .size([w, h])
	    .linkDistance(150)
	    .charge(-1000)
	    .on("tick", tick)
	    .start();
	
	var svg = d3.select("#data_map").append("svg:svg")
	    .attr("width", w)
	    .attr("height", h);
	
	// Per-type markers, as they don't inherit styles.
	svg.append("svg:defs").selectAll("marker")
	    .data(["suit", "licensing", "resolved"])
	  .enter().append("svg:marker")
	    .attr("id", String)
	    .attr("viewBox", "0 -5 10 10")
	    .attr("refX", 15)
	    .attr("refY", -1.5)
	    .attr("markerWidth", 6)
	    .attr("markerHeight", 6)
	    .attr("orient", "auto")
	  .append("svg:path")
	    .attr("d", "M0,-5L10,0L0,5");
	
	var path = svg.append("svg:g").selectAll("path")
	    .data(force.links())
	  .enter().append("svg:path")
	    .attr("class", function(d) { return "link suit"; })
	    .attr("marker-end", function(d) { return "url(#suit)"; });
	
	var circle = svg.append("svg:g").selectAll("circle")
	    .data(force.nodes())
	  .enter().append("svg:circle")
	    .attr("r", 6)
	    .attr("fill",function(d){return colours[licenses[d.name]];})
	    .call(force.drag)
	    .on("click",function(d){alert(d.name+"\nLicence: "+licenses[d.name])});
	
	var text = svg.append("svg:g").selectAll("g")
	    .data(force.nodes())
	  .enter().append("svg:g");
	
	// A copy of the text with a thick white stroke for legibility.
	text.append("svg:text")
	    .attr("x", 8)
	    .attr("y", ".31em")
	    .attr("class", "shadow")
	    .text(function(d) { return d.name; });
	
	text.append("svg:text")
	    .attr("x", 8)
	    .attr("y", ".31em")
	    .text(function(d) { return d.name; });
	
	// Use elliptical arc path segments to doubly-encode directionality.
	function tick() {
	  path.attr("d", function(d) {
	    var dx = d.target.x - d.source.x,
	        dy = d.target.y - d.source.y,
	        dr = 0;//Math.sqrt(dx * dx + dy * dy);
	    return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
	  });
	
	  circle.attr("transform", function(d) {
	    return "translate(" + d.x + "," + d.y + ")";
	  });
	
	  text.attr("transform", function(d) {
	    return "translate(" + d.x + "," + d.y + ")";
	  });
	}
	

}