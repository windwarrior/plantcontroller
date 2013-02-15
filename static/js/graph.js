// Constructor for new Graph
function Graph(canvasId, graphType, horDataPoints, vertDataPoints, interval, offset, ratio){
    this.canvasId = canvasId;
    this.graphType = graphType;
    this.interval = interval;
    this.offset = offset;
    this.horDataPoints = horDataPoints;
    this.vertDataPoints = vertDataPoints;
    this.ratio = ratio;

    this.update();

}

// Draws a grid for the current Graph, uses a canvas to draw to
Graph.prototype.paintGrid = function(){
    var ctx = $(this.canvasId).get(0).getContext('2d');
    ctx.beginPath();

    // Draw the box around the grid
    ctx.rect(this.borderWidth, this.borderHeight, this.graphWidth, this.graphHeight);
    ctx.stroke();

    ctx.beginPath();
    ctx.strokeStyle = "#777"
    // Draw the horizontal lines of the grid
    for (var i=1; i<this.vertDataPoints; i++){
       ctx.moveTo(this.borderWidth, this.borderHeight + i * this.heightUnit)
       ctx.lineTo(this.width - this.borderWidth, this.borderHeight + i * this.heightUnit);
    }     

    // Draw the vertical lines of the grid
    for (var j=1; j<this.horDataPoints; j++){
       ctx.moveTo(this.widthUnit * (j) + this.borderWidth, this.borderHeight)
       ctx.lineTo(this.widthUnit * (j) + this.borderWidth, this.height - this.borderHeight);
    }  
    
    ctx.stroke();
} 


// Functie die gecalled wordt om het grid te restoren
// Calculates some new variables for the scaling layout
Graph.prototype.update = function(){
    this.width = $(this.canvasId).parent().width();
    this.height = Math.floor(this.width * this.ratio);

    $(this.canvasId).attr('width', this.width).attr('height', this.height);

    this.borderHeight = this.height / (this.vertDataPoints + 2);
    this.borderWidth = this.width / (this.horDataPoints + 2);

    this.graphWidth = (this.width - this.borderWidth*2);
    this.graphHeight =  (this.height - this.borderHeight*2); 

    this.widthUnit = this.graphWidth / (this.horDataPoints-1);
    this.heightUnit = this.graphHeight / (this.vertDataPoints-1);

    //Repaint the grid, vertical legenda, the static parts of the graph
    this.paintGrid();  
    this.paintVerticalLegenda();
  
}

//Functie die gecalled wordt als er een nieuw datapunt opgevraagd moet worden
Graph.prototype.updateData = function(){
    var me = this;

    console.log("Updating! " + this.canvasId);

    $.jsonRPC.request('getDataPoints', {
        params: [me.graphType, me.interval, me.horDataPoints, me.offset],
        success: function(result) {
            me.update();
            me.drawGraph(result.result);
        },
        error: function(result) {
            console.log(result);
        }
    });
}

// Called when the canvas gets resized, update the current variables (width, height) and repaint the graphs
Graph.prototype.onResize = function(){
    this.update();

    this.drawGraph(this.dataDict);
}

// Draw the graph on the canvas, this function takes the exact dict that is fetched using JSONRPC getDataPoints()
Graph.prototype.drawGraph = function(dataDict){
    this.dataDict = dataDict;
    var ctx = $(this.canvasId).get(0).getContext('2d');

    ctx.strokeStyle = '#f00';
    ctx.lineWidth = 3;
    ctx.beginPath();

    // Draw the graph if there are points and the length greater then 0
    if(dataDict["points"] && dataDict["points"].length > 0){
        // Move to the first datapoint
        var yPos = (this.borderHeight + this.graphHeight) - (dataDict["points"][0]["datapoint"]/dataDict["adc_max"] * this.graphHeight);
        ctx.moveTo(this.borderWidth, yPos);
    
        // For the lenght of the datapoints, make lines to the next datapoints
        for(var j=1; j<dataDict["points"].length; j++){
            var newyPos = (this.borderHeight + this.graphHeight) - (dataDict["points"][j]["datapoint"]/dataDict["adc_max"] * this.graphHeight);
            ctx.lineTo(this.borderWidth + j * this.widthUnit, newyPos);            
        }

        ctx.stroke();        

        // Draw green dots on the datapoints
        for(var i=0; i<dataDict["points"].length; i++){
            var yPos = (this.borderHeight + this.graphHeight) - (dataDict["points"][i]["datapoint"]/dataDict["adc_max"] * this.graphHeight);
            ctx.beginPath();
            ctx.arc(this.borderWidth + i * this.widthUnit, yPos, this.widthUnit * 0.1, 0, Math.PI * 2);
            ctx.fillStyle = 'green';
            ctx.fill();
            ctx.lineWidth = 1;
            ctx.strokeStyle = '#003300';
            ctx.stroke();
        }
        
        // Draw the times below the graph
        this.paintHorizontalLegenda(dataDict);
    }
}

// Draws the vertical legenda, from 0 to 1, should someday be called with basereading, so that it draws a real variable (Ohm/Lumen/..) instead of relative values
Graph.prototype.paintVerticalLegenda = function(){
    var ctx = $(this.canvasId).get(0).getContext('2d')
    ctx.beginPath();
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'black';
    ctx.fillStyle = 'black';
    ctx.textBaseline = 'middle';

    var legendaUnit = 1.0/(this.vertDataPoints-1);

    for (var i=0; i<this.vertDataPoints; i++){
        ctx.fillText((1.0 - i * legendaUnit).toFixed(2), 0.5 * this.borderWidth, this.heightUnit * (i) + this.borderHeight, this.widthUnit);
    }
    ctx.stroke();  
}

// Draws times below the graph, 12:40, 12:45.. etc.
Graph.prototype.paintHorizontalLegenda = function(dataDict){
    var ctx = $(this.canvasId).get(0).getContext('2d');
    ctx.beginPath();
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'black';
    ctx.fillStyle = 'black';
    ctx.textBaseline = 'middle';

    // For each time in the graph, draw it below a datapoint in the graph
    for (var i=0; i<this.dataDict["points"].length; i++){
        ctx.fillText(dataDict["points"][i]["time"], this.widthUnit * (i) + this.borderWidth, this.height - 0.5 * this.borderHeight, this.widthUnit * 0.9);
    }

    ctx.stroke();  
}
           
