using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class move : MonoBehaviour {
	//private Vector3 position;
	// Use this for initialization
	static public string lastReceivedUDPPacket;

	// Update is called once per frame
	void Update () 
	{
		//Vector3 position = Vector3.zero;


		if(Server.lastReceivedUDPPacket != "")
		{
			try
			{
				float xpos = float.Parse (Server.lastReceivedUDPPacket);
				transform.position = new Vector3(xpos, 0, 0);

			}
			catch
			{
				
			}

		}
		Server.lastReceivedUDPPacket = "";
		if (Server.allReceivedUDPPackets.Length > 40) 
		{
			Server.allReceivedUDPPackets = "";
		}
			



	}
		

}	
