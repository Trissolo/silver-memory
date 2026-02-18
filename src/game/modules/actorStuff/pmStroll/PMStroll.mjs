// Phaser.Math.Vector2
// Phaser.Math.Distance.BetweenPoints
const {Vector2, Distance: {BetweenPoints: heuristic}} = Phaser.Math;

// Phaser.Geom.Polygon;
// Phaser.Geom.Line;
// Phaser.Geom.Line.GetMidPoint;
// Phaser.Geom.Intersects.LineToLine;
const {Polygon, Line, Line: {GetMidPoint}, Intersects: {LineToLine}} = Phaser.Geom;

// generators:
import AnyAgainstAllOthers from "./generators/AnyAgainstAllOthers.mjs";
import EachPolygonSide from "./generators/EachPolygonSide.mjs";
import EachVectorAndAdjacents from "./generators/EachVectorAndAdjacents.mjs";

import SnappedCoord from "./generators/snappedCoord.mjs";


// graph
import GraphManager from "./GraphManager.mjs";

// pathf algos
// import Dijkstra from "./pathfinding/Dijkstra.mjs";

import AStar from "./pathfinding/AStar.mjs";

// debug
import PMDebug from "./pmdebug/PMDebug.mjs";


export default class PMStroll
{
    // optional:
    // debug;

    // defaults:
    static epsilon = 0.03;

    static splitAmount = 5;

    // for recycle:
    static vertexA = new Vector2();

    static vertexB = new Vector2();

    static out = new Vector2();

    static useDebug(scene)
    {
        this.debug = new PMDebug(scene);
        
        return this;
    }

    // test simple add

    static addVisibilityMap(aryOfPhaserPolygonParams)
    {
        // 'Build" the VisibilityMap
        const graph = new Map();
        
        const polygons = [];

        for (const phaserPolygonParams of aryOfPhaserPolygonParams)
        {
            polygons.push(new Polygon(phaserPolygonParams));
        }

        const visMap = {graph, polygons};

        //bui

        this.grabConcave(visMap)
            .checkAdjacent(visMap)
            .connectNodes(visMap);

        return visMap;
    }

    static grabConcave(visibilityMap)
    {
        const {vertexA, vertexB} = this;
        
        let isFirstPoly = true;
        
        //iterate all walkable poly
        for (const {points} of visibilityMap.polygons)
        {
            //iterate all vertices in each poly
            for(const [curr, succ, prec] of EachVectorAndAdjacents(points))
            {    
                vertexA.copy(succ).subtract(curr);

                vertexB.copy(curr).subtract(prec);
     
                if( (vertexB.cross(vertexA) < 0) === isFirstPoly )
                {
                    GraphManager.addNode(curr, visibilityMap.graph);
                }   
            }
            
            // The fist polygon - the walkable one - has been checked. The remaining obstacle-polys need 'isFirstPoly' to be false
            isFirstPoly = false;
        
        }

        return this;
        
    } // end grabConcave

    static checkAdjacent(visibilityMap)
    {
        const {graph} = visibilityMap;

        for (const {points} of visibilityMap.polygons)
        {
            // EachPolygonSide
            for (const [sidePointA, sidePointB] of EachPolygonSide(points))
            {
                if (graph.has(sidePointA) && graph.has(sidePointB))
                {
                    GraphManager.addEdge(sidePointA, sidePointB, heuristic(sidePointA, sidePointB), graph);
                }
            }
        }

        return this;

    } // end checkAdjacent

    static connectNodes(visibilityMap, graph = visibilityMap.graph)
    {
        for (const [concaveA, concaveB] of AnyAgainstAllOthers([...graph.keys()]))
        {
            if (this.quickInLineOfSight(concaveA, concaveB, visibilityMap))
            {
                GraphManager.addEdge(concaveA, concaveB, heuristic(concaveA, concaveB), graph);
            }
        }
    }

    static quickInLineOfSight(start, end, visibilityMap)
    {
        //the segment to check against any polygon side
        const ray = new Line().setFromObjects(start, end);

        //One side of current polygon
        const polygonSide = new Line();

        // internal recycled Vector2
        const tempVec = new Vector2();

        for (const {points} of visibilityMap.polygons)
        {
            for (const [sidePointA, sidePointB] of EachPolygonSide(points))
            {
                polygonSide.setFromObjects(sidePointA, sidePointB);

                if (LineToLine(ray, polygonSide, this.out) && !this.itsNear(start, end, sidePointA, sidePointB, tempVec))
                {
                    return false;
                }
            }
        }

        //another loop?
        const rayPoints = ray.getPoints(this.splitAmount);

        rayPoints[0] = GetMidPoint(ray);

        let isFirstAgain = false;

        for (const poly of visibilityMap.polygons)
        {
            if (rayPoints.some(this.isContained, poly) === isFirstAgain)
            {
                return false;
            }

            isFirstAgain = true;
        }

        return true;

    } // end quickInLineOfSight

    static itsNear(rayA, rayB, sideA, sideB, recycledVec = new Vector2())
    {
        return (recycledVec.setFromObject(rayA).fuzzyEquals(sideA, this.epsilon) || recycledVec.setFromObject(rayB).fuzzyEquals(sideB, this.epsilon)) || (recycledVec.setFromObject(rayB).fuzzyEquals(sideA, this.epsilon) || recycledVec.setFromObject(rayA).fuzzyEquals(sideB, this.epsilon));
    }

    static isContained(point) //, idx, ary)
    {
        return this.contains(point.x, point.y);
    }

    static prepareGraph(start, end, visibilityMap)
    {
        // 1) clone the base Graph:
        const clonedGraph = GraphManager.cloneGraph(visibilityMap.graph);

        // 2) get the vertices to be checked against the new one
        const graphKeys = [...clonedGraph.keys()];

        // 3) create edge if needed
        for (const newVertex of [start, end])
        {
            GraphManager.addNode(newVertex, clonedGraph);

            for (const existingVertex of graphKeys)
            {
                /// GAGG!
                // if (newVertex === start)
                // {
                //     GraphManager.addEdge(newVertex, existingVertex, heuristic(newVertex, existingVertex), clonedGraph);
                //     continue;
                // }
                /// end GAGG
                if (this.quickInLineOfSight(newVertex, existingVertex, visibilityMap))
                {
                    GraphManager.addEdge(newVertex, existingVertex, heuristic(newVertex, existingVertex), clonedGraph);
                }
            }

            // From now, the 'newVertex' belongs in the graph, so add it to be checked against the next vertex
            graphKeys.push(newVertex);
        }

        // // 4 mental check :/
        // const tempRect = new Phaser.Geom.Rectangle(start.x - 12, start.y - 12, 24, 24);
        // const tempEdge = new Phaser.Geom.Line();
        // console.log("START in CLonedGr", clonedGraph.has(start));
        // // console.log("start", start, "Rect:", tempRect);
        // // console.log("start", start.x, start.y, "Rect:", tempRect.x, tempRect.y);
        // for (const poly of visibilityMap.polygons)
        // {
        //     for (const [varA, varB] of EachPolygonSide(poly.points))
        //     {
        //         tempEdge.setFromObjects(varA, varB);

        //         // console.log(tempEdge, Phaser.Geom.Intersects.LineToRectangle(tempEdge, tempRect));
                
        //         if (Phaser.Geom.Intersects.LineToRectangle(tempEdge, tempRect))
        //         {
                        
        //                 console.log("Intersect found!!!!!!!!!!!!!!!!!!!!!!!!!", varA, varB);
        //                 if ( !clonedGraph.has(start) )
        //                 {
        //                     GraphManager.addNode(start, clonedGraph)
        //                 }
                        
        //                 if (!clonedGraph.has(varA))
        //                 {
        //                     GraphManager.addNode(varA, clonedGraph);
        //                 }

        //                 if (!clonedGraph.has(varB))
        //                 {
        //                     GraphManager.addNode(varB, clonedGraph);
        //                 }
        //                 GraphManager.addEdge(start, varA, heuristic(start, varA), clonedGraph);
        //                 GraphManager.addEdge(start, varB, heuristic(start, varB), clonedGraph);
        //                 console.log("HAS", clonedGraph.has(start), clonedGraph.has(varA), clonedGraph.has(varB));
        //         }
        //             //graphKeys.push(varA);
        //             //GraphManager.addEdge(varA, start, heuristic(varA, start), clonedGraph);
        //             //GraphManager.addEdge(varB, start, heuristic(varB, start), clonedGraph);
        //             //graphKeys.push(varB);
        //     }
        //         // else
        //         // {
        //         //     console.log("None found");
        //         // }
        
            
        // }

        return clonedGraph;
    }

    static pathDijkstra(start, end, visibilityMap)
    {
        // disposable clones of the two new vertices, although I'm not sure garbage collection will benefit from them
        start = {x: start.x, y: start.y};

        end = {x: end.x, y: end.y};

        const clonedGraph = this.prepareGraph(start, end, visibilityMap);

        return new Dijkstra(start, end, clonedGraph).search();

    }  // end pathDijkstra

    static pathAStar(start, end, visibilityMap)
    {
        // disposable clones of the two new vertices, although I'm not sure garbage collection will benefit from them
        start = {x: start.x, y: start.y};
        
        end = {x: end.x, y: end.y};

        const clonedGraph = this.prepareGraph(start, end, visibilityMap);

        return new AStar(start, end, clonedGraph, heuristic).search();

    } // end pathAStar

    static calculatePath(start, end, visibilityMap)
    {
        // disposable clones of the two new vertices, although I'm not sure garbage collection will benefit from them
        start = {x: start.x, y: start.y};
        
        end = {x: end.x, y: end.y};

        const clonedGraph = this.prepareGraphWithTrick(start, end, visibilityMap);

        return new AStar(start, end, clonedGraph, heuristic).search();

    } // end calculatePath

    static permittedPosition(point2Like, {polygons})
    {
        for (let i = 0, poly, isFirst = false; i < polygons.length; i++)
        {
            if (polygons[i].contains(point2Like.x, point2Like.y) === isFirst)
            {
                return false;
            }

            isFirst = true;
        }

        return true;
    }


    /**
     * 
     * @param {Phaser.Types.Math.Vector2Like} actor 
     * @param {*} polygonMap 
     * @param {Phaser.Geom.Polygon} walkable 
     */
    static snapIfRequired(actor, polygonMap = actor.polygonalMap, walkable = polygonMap.polygons[0])
    {
        //const walkable = polygonMap.polygons[0];
        // PMStroll.permittedPosition(this.clickVector, player.polygonalMap)
        //if (walkable.contains(actor.x, actor.y))
        if (this.permittedPosition(actor, polygonMap))
        {
            return true;
        }

        const {x: currX, y: currY} = actor;
        const quickVec = new Phaser.Math.Vector2();

        for (const x of SnappedCoord(currX))
        {
            for (const y of SnappedCoord(currY))
            {
                quickVec.set(x, y);

                if (this.permittedPosition(quickVec, polygonMap))
                {
                    console.log("🐠 danger averted", quickVec, quickVec.x - actor.x, quickVec.y - actor.y);
                    actor.x = x;
                    actor.y = y;
                    return actor;
                }
            }
        }

        console.error("🦈 Shit happened! Player outside the polygon Map.");

        return false;
    }

    // getClosestPointOnPolygon(point, polygon)
    // {
    //     let closestPt = new Phaser.Math.Vector2(0, 0);
    //     let minDistance = Infinity;
    //     const points = polygon.points;

    //     for (let i = 0; i < points.length; i++) {
    //         // Get the current segment (start and end points)
    //         let p1 = points[i];
    //         let p2 = points[(i + 1) % points.length]; // Loops back to the start

    //         // Find the closest point on this specific segment
    //         let tempPt = this.getClosestPointOnSegment(point.x, point.y, p1.x, p1.y, p2.x, p2.y);
    //         let dist = Phaser.Math.Distance.Between(point.x, point.y, tempPt.x, tempPt.y);

    //         if (dist < minDistance) {
    //             minDistance = dist;
    //             closestPt.x = tempPt.x;
    //             closestPt.y = tempPt.y;
    //         }
    //     }

    //     // Applying Math.floor/ceil as requested for that "snappy" low-precision feel
    //     return {
    //         x: Math.floor(closestPt.x),
    //         y: Math.floor(closestPt.y)
    //     };
    // }

    static getClosestPointOnSegment(px, py, x1, y1, x2, y2)
    {
        let dx = x2 - x1;
        let dy = y2 - y1;

        if (dx === 0 && dy === 0) return { x: x1, y: y1 };

        // Calculate the projection normalized to the segment length
        let t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);

        // Clamp t to ensure the point is on the segment (0 to 1)
        t = Math.max(0, Math.min(1, t));

        return {
            x: x1 + t * dx,
            y: y1 + t * dy
        };
    }

    static getClosestInVismap(point, visibilityMap)
    {
        let closestPt = new Phaser.Math.Vector2(0, 0);
        let minDistance = Infinity;
        //const points = polygon.points;
        const resLine = new Phaser.Geom.Line();
        let wantedA = null;
        let wantedB = null;

        for (const polygon of visibilityMap.polygons)
        {
            for (const [p1, p2] of EachPolygonSide(polygon.points))
            {
                // Find the closest point on this specific segment
                let tempPt = this.getClosestPointOnSegment(point.x, point.y, p1.x, p1.y, p2.x, p2.y);
                let dist = Phaser.Math.Distance.Between(point.x, point.y, tempPt.x, tempPt.y);

                if (dist < minDistance) {
                    minDistance = dist;
                    closestPt.x = tempPt.x;
                    closestPt.y = tempPt.y;
                    resLine.setFromObjects(p1, p2);
                    wantedA = p1;
                    wantedB = p2;
                    

                }
            }

            // Applying Math.floor/ceil as requested for that "snappy" low-precision feel
            return {
                x: Math.floor(closestPt.x),
                y: Math.floor(closestPt.y),
                line: resLine,
                wantedA,
                wantedB
            };
        }
    }

    static prepareGraphWithTrick(start, end, visibilityMap)
    {
        const {wantedA, wantedB} = this.getClosestInVismap(start, visibilityMap);

        console.log("A SIDE EXISTS:", wantedA, wantedB);

        console.dir(visibilityMap.polygons);

        // 1) clone the base Graph:
        const clonedGraph = GraphManager.cloneGraph(visibilityMap.graph);

        // 2) get the vertices to be checked against the new one
        const graphKeys = [...clonedGraph.keys()];

        console.log("INDEXOF A", graphKeys.indexOf(wantedA));
        console.log("INDEXOF B", graphKeys.indexOf(wantedA));

        const gagset = new Set([wantedA, wantedB])

        // 3) create edge if needed
        for (const newVertex of [start, end])
        {
            GraphManager.addNode(newVertex, clonedGraph);

            for (const existingVertex of graphKeys)
            {
                //console.log("EXists:", gagset.has(existingVertex));
                /// GAGG!
                if (newVertex === start && (gagset.has(existingVertex) || newVertex.x === existingVertex.x && newVertex.y === existingVertex.y))
                {
                    GraphManager.addEdge(newVertex, existingVertex, heuristic(newVertex, existingVertex), clonedGraph);
                    continue;
                }
                /// end GAGG
                if (this.quickInLineOfSight(newVertex, existingVertex, visibilityMap))
                {
                    GraphManager.addEdge(newVertex, existingVertex, heuristic(newVertex, existingVertex), clonedGraph);
                }
            }

            // From now, the 'newVertex' belongs in the graph, so add it to be checked against the next vertex
            graphKeys.push(newVertex);
        }

        // // 4 mental check :/
        // const tempRect = new Phaser.Geom.Rectangle(start.x - 12, start.y - 12, 24, 24);
        // const tempEdge = new Phaser.Geom.Line();
        // console.log("START in CLonedGr", clonedGraph.has(start));
        // // console.log("start", start, "Rect:", tempRect);
        // // console.log("start", start.x, start.y, "Rect:", tempRect.x, tempRect.y);
        // for (const poly of visibilityMap.polygons)
        // {
        //     for (const [varA, varB] of EachPolygonSide(poly.points))
        //     {
        //         tempEdge.setFromObjects(varA, varB);

        //         // console.log(tempEdge, Phaser.Geom.Intersects.LineToRectangle(tempEdge, tempRect));
                
        //         if (Phaser.Geom.Intersects.LineToRectangle(tempEdge, tempRect))
        //         {
                        
        //                 console.log("Intersect found!!!!!!!!!!!!!!!!!!!!!!!!!", varA, varB);
        //                 if ( !clonedGraph.has(start) )
        //                 {
        //                     GraphManager.addNode(start, clonedGraph)
        //                 }
                        
        //                 if (!clonedGraph.has(varA))
        //                 {
        //                     GraphManager.addNode(varA, clonedGraph);
        //                 }

        //                 if (!clonedGraph.has(varB))
        //                 {
        //                     GraphManager.addNode(varB, clonedGraph);
        //                 }
        //                 GraphManager.addEdge(start, varA, heuristic(start, varA), clonedGraph);
        //                 GraphManager.addEdge(start, varB, heuristic(start, varB), clonedGraph);
        //                 console.log("HAS", clonedGraph.has(start), clonedGraph.has(varA), clonedGraph.has(varB));
        //         }
        //             //graphKeys.push(varA);
        //             //GraphManager.addEdge(varA, start, heuristic(varA, start), clonedGraph);
        //             //GraphManager.addEdge(varB, start, heuristic(varB, start), clonedGraph);
        //             //graphKeys.push(varB);
        //     }
        //         // else
        //         // {
        //         //     console.log("None found");
        //         // }
        
            
        // }

        return clonedGraph;
    }

}

// the original 'Phaser.Geom.Line.GetPoints' function, in case it gets changed in the future:
// function GetPoints(line, quantity, stepRate, out)
// {
//     if (out === undefined) { out = []; }

//     //  If quantity is a falsey value (false, null, 0, undefined, etc) then we calculate it based on the stepRate instead.
//     if (!quantity && stepRate > 0)
//     {
//         quantity = Length(line) / stepRate;
//     }

//     var x1 = line.x1;
//     var y1 = line.y1;

//     var x2 = line.x2;
//     var y2 = line.y2;

//     for (var i = 0; i < quantity; i++)
//     {
//         var position = i / quantity;

//         var x = x1 + (x2 - x1) * position;
//         var y = y1 + (y2 - y1) * position;

//         out.push(new Point(x, y));
//     }

//     return out;
// }
