
//Copyright (c) 2012 Jonathan Topf
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in
//all copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
//THE SOFTWARE.

#include <maya/MIOStream.h>
#include <maya/MSimple.h>
#include <maya/MGlobal.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>
#include <maya/MSelectionList.h>
#include <maya/MFnMesh.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MArgList.h>
#include <maya/MString.h>
#include <fstream>


// Use a Maya macro to setup a simple helloWorld class
// with methods for initialization, etc.
//

const MString Version("0.1.1");

DeclareSimpleCommand( ms_export_obj, "mayaseed", Version.asChar());



// All we need to do is supply the doIt method
// which in this case is only a Hello World example
//
MStatus ms_export_obj::doIt( const MArgList& args)
{
    MString mesh_name;
    MString file_path;
    
    //get the args
    
    for (int i = 0; i < args.length(); i++)
    {
        MGlobal::displayInfo(args.asString(i));
        if (args.asString(i) == "-mesh")
        {
            mesh_name = args.asString(i+1);
            
        } else if (args.asString(i) == "-filePath")
        {
            file_path = args.asString(i+1);
        }
    }
    
    
    
    MString display_info;
    display_info.format("Exporting ^1s using ms_export_obj", mesh_name);
	MGlobal::displayInfo(display_info);
    
    MSelectionList sel;
    sel.add(mesh_name);
    MDagPath mesh_dag_path;
    sel.getDagPath(0, mesh_dag_path);
    
    MFnMesh mesh(mesh_dag_path);
    MItMeshPolygon iter_polys(mesh.object());
        
    //open file for writing
    
    std::ofstream out_file;
    out_file.open(file_path.asChar(), ios::trunc); // open file for writing and overwrite previous contents
    out_file << "# File generated by ms_obj_xport version: " << Version.asChar() << "\n\n";
    
    
    //write points to file
    MPointArray point_array;
    mesh.getPoints(point_array);
    
    for (int i=0; i < point_array.length(); i++)
    {
        MPoint point(point_array[i]);
        out_file << "v " << point.x << " " << point.y << " " << point.z << "\n";
    }
    
    //write uvs to disk
    MFloatArray u_array;
    MFloatArray v_array;
    mesh.getUVs(u_array, v_array);
    
    for (int i=0; i < u_array.length(); i++)
    {
        out_file << "vt " << u_array[i] << " " << v_array[i] << "\n";
    }
    
    MFloatVectorArray normal_array;
    mesh.getNormals(normal_array, MSpace::kTransform);
    //write normals
    for (int i=0; i < normal_array.length(); i++)
    {
        out_file << "vn " << normal_array[i].x << " " << normal_array[i].y <<  " " << normal_array[i].z << "\n";
    }
    

    
    
    //itterate over polys
    while (!iter_polys.isDone())
    {
        
        out_file << "f ";
        
        //create values to store temporary poly info
        int vert_count = iter_polys.polygonVertexCount();
        
        for (int i=0; i < vert_count; i++)
        {
            int uv_index;
            iter_polys.getUVIndex(i, uv_index);
            out_file << (iter_polys.vertexIndex(i)+1) << "/" << (uv_index+1) << "/" << (iter_polys.normalIndex(i)+1) << " ";
        }
        
        out_file << "\n";
        iter_polys.next();
    }
    
    out_file.close();
    return MS::kSuccess;
    
}













