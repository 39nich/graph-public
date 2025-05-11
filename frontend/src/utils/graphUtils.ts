
export function distanceToSegment(x: number, y: number, px1: number, py1: number, px2: number, py2: number) {
    const A = x - px1;
    const B = y - py1;
    const C = px2 - px1;
    const D = py2 - py1;

    const dot = A * C + B * D;
    const lenSq = C * C + D * D;
    let param = -1;

    if (lenSq !== 0) {
        param = dot / lenSq;
    }

    let nearestX, nearestY;

    if (param < 0) {
        nearestX = px1;
        nearestY = py1;
    } else if (param > 1) {
        nearestX = px2;
        nearestY = py2;
    } else {
        nearestX = px1 + param * C;
        nearestY = py1 + param * D;
    }

    const dx = x - nearestX;
    const dy = y - nearestY;

    return Math.sqrt(dx * dx + dy * dy);
}

export function getBounds(points: number[][]) {
    const xs = points.map(p => p[0])
    const ys = points.map(p => p[1])
    return {
      xMin: Math.min(...xs),    
      xMax: Math.max(...xs),
      yMin: Math.min(...ys),
      yMax: Math.max(...ys)
    }
}

export function normalize(
    x: number, xMin: number, xMax: number, 
    y: number, yMin: number, yMax: number, 
    canvasWidth: number, canvasHeight: number
) {
    const padding = 40
    const normalizedX = ((x-xMin) / (xMax - xMin)) * (canvasWidth - padding * 2) + padding
    const normalizedY = canvasHeight - ((y - yMin) / (yMax - yMin)) * (canvasHeight - padding * 2) - padding
    console.log("Bounds:", { xMin, xMax, yMin, yMax })
    return [normalizedX, normalizedY]
}