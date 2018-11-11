$(document).ready(function() {
    var row = 0;
    var MINOR_AUTHOR_PERCENTAGE = 1.00;
    var isReversed = false;

    var colorRows = function() {
        $(this).removeClass("odd");

        if (row++ % 2 == 1) {
            $(this).addClass("odd");
        }

        if(this == $(this).parent().find("tr:visible").get(-1)) {
            row = 0;
        }
    }

    // Fix header and set it to the right width.
    var remainingHeaderWidth = ($("div.logo").width() - 4) - ($("div.logo img").innerWidth() + 48)
    $("div.logo p").css("width", remainingHeaderWidth);

    var filterResponsibilities = function() {
        $("table#blame tbody tr td:last-child").filter(function() {
            return parseFloat(this.innerHTML) < MINOR_AUTHOR_PERCENTAGE;
        }).parent().find("td:first-child").each(function() {
            $("div#responsibilities div h3:contains(\"" + $(this).text() + "\")").parent().hide();
        });
    }

    var filterTimeLine = function() {
        $("div#timeline table.git tbody tr").filter(function() {
            return $(this).find("td:has(div)").length == 0;
        }).hide();
    }

    $("table#changes tbody tr td:last-child").filter(function() {
        return parseFloat(this.innerHTML) < MINOR_AUTHOR_PERCENTAGE;
    }).parent().hide();

    $("table#blame tbody tr td:last-child").filter(function() {
        return parseFloat(this.innerHTML) < MINOR_AUTHOR_PERCENTAGE;
    }).parent().hide();

    $("table.git tbody tr:visible").each(colorRows);

    $("table#changes, table#blame").tablesorter({
        sortList: [[0,0]],
        headers: {
            0: { sorter: "text" }
        }
    }).bind("sortEnd", function() {
        $(this).find("tbody tr:visible").each(colorRows);
    });

    $("table#changes thead tr th, table#blame thead tr th").click(function() {
        $(this).parent().find("th strong").remove();
        var parentIndex = $(this).index();

        if (this.isReversed) {
            $(this).append("<strong> &and;</strong>");
        } else {
            $(this).append("<strong> &or;</strong>");
        }
        this.isReversed = !this.isReversed;
    });

    $("table#changes thead tr th:first-child, table#blame thead tr th:first-child").each(function() {
        this.isReversed = true;
        $(this).append("<strong> &or;</strong>");
    });

    $("table.git tfoot tr td:first-child").filter(function() {
        this.hiddenCount = $(this).parent().parent().parent().find("tbody tr:hidden").length;
        return this.hiddenCount > 0;
    }).each(function() {
        $(this).addClass("hoverable");
        this.innerHTML = "{show_minor_authors} (" + this.hiddenCount + ") &or;";
    }).click(function() {
        this.clicked = !this.clicked;

        if (this.clicked) {
            this.innerHTML = "{hide_minor_authors} (" + this.hiddenCount + ") &and;";
            $(this).parent().parent().parent().find("tbody tr").show().each(colorRows);
        } else {
            this.innerHTML = "{show_minor_authors} (" + this.hiddenCount + ") &or;";
            $(this).parent().parent().parent().find("tbody tr td:last-child").filter(function() {
                return parseFloat(this.innerHTML) < MINOR_AUTHOR_PERCENTAGE;
            }).parent().hide();
            $("table.git tbody tr:visible").each(colorRows);
        }
    });

    filterResponsibilities();
    var hiddenResponsibilitiesCount = $("div#responsibilities div h3:hidden").length;
    if (hiddenResponsibilitiesCount > 0) {
        $("div#responsibilities div h3:visible").each(colorRows);
        $("div#responsibilities").prepend("<div class=\"button\">{show_minor_authors} (" + hiddenResponsibilitiesCount + ") &or;</div>");

        $("div#responsibilities div.button").click(function() {
            this.clicked = !this.clicked;
            if (this.clicked) {
                this.innerHTML = "{hide_minor_authors} (" + hiddenResponsibilitiesCount + ") &and;";
                $("div#responsibilities div").show();
            } else {
                this.innerHTML = "{show_minor_authors} (" + hiddenResponsibilitiesCount + ") &or;";
                filterResponsibilities();
            }
        });
    }


    filterTimeLine();
    var hiddenTimelineCount = $("div#timeline table.git tbody tr:hidden").length;
    if (hiddenTimelineCount > 0) {
        $("div#timeline table.git tbody tr:visible").each(colorRows);
        $("div#timeline").prepend("<div class=\"button\">{show_minor_rows} (" + hiddenTimelineCount + ") &or;</div>");

        $("div#timeline div.button").click(function() {
            this.clicked = !this.clicked;
            if (this.clicked) {
                this.innerHTML = "{hide_minor_rows} (" + hiddenTimelineCount + ") &and;";
                $("div#timeline table.git tbody tr").show().each(colorRows);
            } else {
                this.innerHTML = "{show_minor_rows} (" + hiddenTimelineCount + ") &or;";
                filterTimeLine();
                $("div#timeline table.git tbody tr:visible").each(colorRows);
            }
        });
    }

    $("#blame_chart, #changes_chart").bind("plothover", function(event, pos, obj) {
        if (obj) {
            var selection = "table tbody tr td:contains(\"" + obj.series.label + "\")";
            var element = $(this).parent().find(selection);

            if (element) {
                if (this.hoveredElement && this.hoveredElement.html() != element.parent().html()) {
                    this.hoveredElement.removeClass("piehover");
                }

                element.parent().addClass("piehover");
                this.hoveredElement = element.parent();
            }
        } else if (this.hoveredElement) {
            this.hoveredElement.removeClass("piehover");
        }
    });
});

function generate_pie(group, radius, data, value_fun, color_fun) {
    // Generator for the pie
    var pie_maker = d3.pie().value(value_fun);

    // Generator for the arcs
    var arc_maker = d3.arc().innerRadius(radius/2.5).outerRadius(radius);

    // Generate groups
    var arcs = group.selectAll("arc")
        .data(pie_maker(data))
        .enter()
        .append("g")
        .attr("class", "arc");

    // Draw arc paths
    arcs.append("path")
        .attr("id", function(d, i) { return "path_" + i; })
        .attr("fill", color_fun)
        .attr("stroke", "white")
        .attr("d", arc_maker);

    return arcs;
}

function recolor_table_rows(id) {
    var cpt = 0;
    d3.selectAll("table#" + id + " tbody tr").each(function() {
        var elem = d3.select(this);
        if (this.style["display"] == "") {
            this.className = (cpt % 2 == 0) ? "even" : "odd";
            cpt++;
        }
    });
}

function generate_sortable_table(id, titles, data, filter) {
    var thead = d3.select("table#" + id + " thead"),
        tbody = d3.select("table#" + id + " tbody");

    // Create lines of table
    var lines = tbody.selectAll()
        .data(data)
        .enter()
        .append("tr")
        .attr("id", function (d,i) { return "line_" + i; });

    // Fill the lines with data
    titles.forEach(function (t) {
        lines.append("td").html(function(d) { return d[t]; });
    });
    lines.append("td").filter(filter)
        .append("svg")
        .attr("width", 30).attr("height", 30)
        .append("rect")
        .attr("x", 5).attr("y", 5)
        .attr("width", 15).attr("height", 15)
        .attr("fill", function(d,i) { return d.color; });

    // Hide authors with minimal involvement
    var filtered_lines = lines.filter(function (d) { return !filter(d); });
    filtered_lines.style("display", "none");
    recolor_table_rows(id);

    // Display these same authors when clicking on footer
    if (filtered_lines.size() > 0) {
        var th = d3.select("table#" + id + " tfoot tr th");
        var th_txt = "Display minor authors (" + filtered_lines.size() + ")";
        th.text(th_txt);
        th.on("click", function(d) {
            if (this.className == "visible") {
                filtered_lines.style("display", "none");
                recolor_table_rows(id);
                d3.select(this).text(th_txt);
                this.className = "";
            } else {
                filtered_lines.style("display", "");
                recolor_table_rows(id);
                d3.select(this).text("Hide minor authors");
                this.className = "visible";
            }
        });
    }

    // Make the columns sortable
    d3.selectAll("table#" + id + " tr th").data(titles).on("click", function(d) {
        if (this.className == "asc") {
            lines.sort(function(a, b) { return b[d] > a[d]; });
            recolor_table_rows(id);
            this.className = "desc";
        } else {
            lines.sort(function(a, b) { return b[d] < a[d]; });
            recolor_table_rows(id);
            this.className = "asc";
        }
    });

    return lines;
}

function link_table_and_pie(lines, arcs) {
    var length = arcs.size();
    arcs.on("mouseover", function(d, i){
        if (i+1 != length) {
            d3.select(this).select("path").attr("fill", d3.color(d.data.color).brighter());
            lines.filter(function () { return this.id == ("line_" + i)}).classed("hovered", true);
        }
    });
    arcs.on("mouseout", function(d, i){
        if (i+1 != length) {
            d3.select(this).select("path").attr("fill", d.data.color);
            lines.filter(function () { return this.id == ("line_" + i)}).classed("hovered", false);
        }
    });

    // Link lines with pie chart sections
    lines.on("mouseover", function(d, i){
        d3.select(this).classed("hovered", true);
        if (i+1 != length) {
            arcs.select("#path_" + i).attr("fill", d3.color(d.color).brighter());
        }
    });
    lines.on("mouseout", function(d, i){
        d3.select(this).classed("hovered", false);
        if (i+1 != length) {
            arcs.select("#path_" + i).attr("fill", d.color);
        }
    });
}

function generate_table(div, id, data) {
    var tbody = div.append("table").attr("id", id)
        .classed("git2", "true").append("tbody");

    var lines = tbody.selectAll()
        .data(data).enter()
        .append("tr")
        .attr("id", function (d,i) { return "line_" + i; });
    Object.keys(data[0]).forEach(function(t) {
        var td = lines.append("td")
            .html(function(d) { return d[t];})
            .each(function(d) { if (t == "severity")
                d3.select(this).classed(d[t],true);
                               });
    });
    recolor_table_rows(id);
}

function make_box_hideable(label_id, box_id, display) {
    d3.select("div#" + label_id).on("click", function () {
        if (this.className == "git2 visible") {
            d3.select("div#" + box_id).style("display", "none");
            d3.select(this).style("transform", "rotate(0deg) translate(-50px,-15px)");
            this.className = "git2";
        } else {
            d3.select("div#" + box_id).style("display", display);
            d3.select(this).style("transform", "rotate(90deg) translate(-10px,10px)");
            this.className = "git2 visible";
        }
    });
}
