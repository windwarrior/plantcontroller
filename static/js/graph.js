function Graph(canvasId, graphType, horDataPoints, vertDataPoints, interval, offset){
    this.canvasId = canvasId;
    this.graphType = graphType;
    this.interval = interval;
    this.offset = offset;
    this.horDataPoints = horDataPoints;
    this.vertDataPoints = vertDataPoints;

    this.update();

}

Graph.prototype.paintGrid = function(){
    var ctx = $(this.canvasId).get(0).getContext('2d');
    ctx.beginPath();

    ctx.rect(this.borderWidth, this.borderHeight, this.graphWidth, this.graphHeight);
    ctx.stroke();

    ctx.beginPath();
    ctx.strokeStyle = "#777"
    // hor
    for (var i=1; i<this.vertDataPoints; i++){
       ctx.moveTo(this.borderWidth, this.borderHeight + i * this.heightUnit)
       ctx.lineTo(this.width - this.borderWidth, this.borderHeight + i * this.heightUnit);
    }     

    // vert
    for (var j=1; j<this.horDataPoints; j++){
       ctx.moveTo(this.widthUnit * (j) + this.borderWidth, this.borderHeight)
       ctx.lineTo(this.widthUnit * (j) + this.borderWidth, this.height - this.borderHeight);
    }  
    
    ctx.stroke();
} 


//Functie die gecalled wordt om het grid te restoren
Graph.prototype.update = function(){
    this.width = $(this.canvasId).parent().width();
    this.height = Math.floor(this.width * 0.5);

    $(this.canvasId).attr('width', this.width).attr('height', this.height);

    this.borderHeight = 0.1 * this.height;
    this.borderWidth = 0.1 * this.width;

    this.graphWidth = (this.width - this.borderWidth*2);
    this.graphHeight =  (this.height - this.borderHeight*2); 

    this.widthUnit = this.graphWidth / (this.horDataPoints-1);
    this.heightUnit = this.graphHeight / (this.vertDataPoints-1);

    this.paintGrid();  
    this.paintVerticalLegenda();
  
}

//Functie die gecalled wordt als er een nieuw datapunt opgevraagd moet worden
Graph.prototype.updateData = function(){
    var me = this;

    $.jsonRPC.request('getDataPoints', {
        params: [me.interval, me.horDataPoints, me.offset],
        success: function(result) {
            console.log(result.result);
            me.update();
            me.drawGraph(result.result);
        },
        error: function(result) {
            console.log(result);
        }
    });
}

Graph.prototype.onResize = function(){
    this.update();

    this.drawGraph(this.dataDict);
}

Graph.prototype.drawGraph = function(dataDict){
    this.dataDict = dataDict;
    var ctx = $(this.canvasId).get(0).getContext('2d');

    ctx.strokeStyle = '#f00';
    ctx.lineWidth = 3;
    ctx.beginPath();

    if(dataDict && dataDict.length > 0){
        var yPos = (this.borderHeight + this.graphHeight) - (dataDict[0]["datapoint"] * this.graphHeight);
        ctx.moveTo(this.borderWidth, yPos);
    
        for(var j=1; j<dataDict.length; j++){
            var newyPos = (this.borderHeight + this.graphHeight) - (dataDict[j]["datapoint"] * this.graphHeight);
            ctx.lineTo(this.borderWidth + j * this.widthUnit, newyPos);            
        }

        ctx.stroke();        
    }

    for(var i=0; i<dataDict.length; i++){
        var yPos = (this.borderHeight + this.graphHeight) - (dataDict[i]["datapoint"] * this.graphHeight);
        ctx.beginPath();
        ctx.arc(this.borderWidth + i * this.widthUnit, yPos, this.widthUnit * 0.1, 0, Math.PI * 2);
        ctx.fillStyle = 'green';
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#003300';
        ctx.stroke();
    }

    this.paintHorizontalLegenda(dataDict);
}

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


Graph.prototype.paintHorizontalLegenda = function(dataDict){
    var ctx = $(this.canvasId).get(0).getContext('2d');
    ctx.beginPath();
    ctx.textAlign = 'center';
    ctx.strokeStyle = 'black';
    ctx.fillStyle = 'black';
    ctx.textBaseline = 'middle';

    for (var i=0; i<this.dataDict.length; i++){
        ctx.fillText(dataDict[i]["time"], this.widthUnit * (i) + this.borderWidth, this.height - 0.5 * this.borderHeight, this.widthUnit);
    }

    ctx.stroke();  

}
           
