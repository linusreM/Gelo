using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]

public class PGrid : MonoBehaviour {

	public int xSize, ySize; //Gridsize

	public int startX, startY; //Starting point for raising vertices
	public float height = 4.0f;

	private Mesh mesh;
	private Vector3[] vertices;


	private void Awake(){
		Generate ();
	}

	void Update(){			//Contains a short test of realtime update of vertices
		MoveVertex(Vector3.up * height, startX, 0); 
		startX = (startX +1)%(((xSize+1)*(ySize+1))); //+1%Clamp
	}
	private void Generate(){ 		//Generates the grid

		GetComponent<MeshFilter>().mesh = mesh = new Mesh();
		mesh.name = "Procedural Grid";

		vertices = new Vector3[(xSize + 1) * (ySize + 1)];		//Generates vertexes, distance between is one unit
		for (int y = 0, i = 0; y <= ySize; y++) {
			for (int x = 0; x <= xSize; x++, i++) {
				vertices [i] = new Vector3 (x, 0, y);
			}
		}

		int[] tris = new int[xSize * ySize * 6];				//Sets up the triangles, assignment in clockwise order
		for (int ti = 0, vi = 0, y = 0; y < ySize; y++, vi++) {
			for(int x = 0; x < xSize; x++, ti += 6, vi++){
				tris[ti] = vi;
				tris[ti+3] = tris[ti+2] = vi + 1;
				tris[ti+4] = tris[ti+1] = vi + xSize + 1;
				tris[ti+5] = vi + xSize + 2;
			}
			mesh.vertices = vertices;
			mesh.triangles = tris;

		}
	}
	private void MoveVertex(Vector3 move, int xIndex, int yIndex){ //Edit a vertex in the grid based on x-y index
		mesh = GetComponent<MeshFilter> ().mesh;
		Vector3[] verts = mesh.vertices;
		int index = xIndex + (yIndex * xSize);
		verts[index] += move;
		mesh.vertices = verts;		//Reassign
		mesh.RecalculateBounds();
		mesh.RecalculateNormals();
	}
}
