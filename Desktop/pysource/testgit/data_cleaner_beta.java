/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 *
 * @author netklause
 */
public class data_cleaner_beta {
    
    private static final String COMMA_DELIMITER = ",";
    private static final String NEW_LINE_SEPARATOR = "\n";
    private static final String FILE_HEADER = "SrcAddr,DstAddr,Proto,Sport,Dport,"
            + "State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,"
            + "dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,"
            + "SAppBytes,DAppbytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,"
            + "DstRate,Tag";
    public static String fileName_read;
    public static String fileName_write;
    public static String line = "";

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, IOException{
        // TODO code application logic here
        int lineCount = 1;
        fileName_read = args[0];
        fileName_write = args[1];
   
        
        BufferedReader fileReader = null;
        fileReader = new BufferedReader(new FileReader(fileName_read));
        fileReader.readLine();
        
        FileWriter fileWriter = null;
        fileWriter = new FileWriter(fileName_write);
        fileWriter.append(FILE_HEADER.toString());
        fileWriter.append(NEW_LINE_SEPARATOR);
        
        
        while ((line = fileReader.readLine()) != null) {
            lineCount++;
            String[] tokens = line.split(COMMA_DELIMITER); // breakdown this line into tokens
            int col_count = 1;
            String tempLine = "";
            Boolean isValid = true;
          
            
            for(String cell : tokens) { // scan through this line
                
                     
                if(cell.equals("") && (col_count == 6 || col_count == 20 || col_count == 22 || col_count == 27 || col_count == 28)) { // Selected columns
                    //System.out.println(lineCount);
                    tempLine+="0"; // padding the cell
                    tempLine+=",";
                    isValid = false;
                    break;
                } else { // this line has no blank cell
                    
                    if(col_count==13 || col_count==14) // StartTime, LastTime
                        cell = cell.substring(0, 6) + "20" + cell.substring(6, cell.length());
                    
                    tempLine+=cell; // concatenate cell into this line
                    
                    if(col_count<33) 
                        tempLine+=",";
                }
                col_count++;
            }
            
            //if(isValid) {
                fileWriter.append(tempLine);
                fileWriter.append(NEW_LINE_SEPARATOR);
            //}          
            
        }
        
        fileWriter.flush();
        fileWriter.close();
       
        
    
    }
    
}
