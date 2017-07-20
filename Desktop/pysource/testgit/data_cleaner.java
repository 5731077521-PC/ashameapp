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
public class data_cleaner {
    
    private static final String COMMA_DELIMITER = ",";
    private static final String NEW_LINE_SEPARATOR = "\n";
    private static final String FILE_HEADER = "SrcAddr,DstAddr,Proto,Sport,Dport,"
            + "State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,"
            + "dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,"
            + "SAppBytes,DAppbytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,"
            + "DstRate,Tag";
    public static String fileName_read = "/home/netklause/Desktop/data/";
    public static String fileName_write = "/home/netklause/Desktop/data/";
    public static String line = "";

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, IOException{
        // TODO code application logic here
        int lineCount = 1;
        fileName_read += args[0];
        fileName_write += args[1];
   
        
        BufferedReader fileReader = null;
        fileReader = new BufferedReader(new FileReader(fileName_read));
        fileReader.readLine();
        
        FileWriter fileWriter = null;
        fileWriter = new FileWriter(fileName_write);
        fileWriter.append(FILE_HEADER.toString());
        fileWriter.append(NEW_LINE_SEPARATOR);
        
        
        while ((line = fileReader.readLine()) != null) {
            lineCount++;
            String[] tokens = line.split(COMMA_DELIMITER);
            int col_count = 0;
            String tempLine = "";
            Boolean isValid = true;
          
            
            for(String cell : tokens) {
                
                     
                if(cell.equals("")) {
                    System.out.println(lineCount);
                    isValid = false;
                    break;
                } else {
                    
                    if(col_count==12 || col_count==13) 
                        cell = cell.substring(0, 6) + "20" + cell.substring(6, cell.length());
                    
                    tempLine+=cell;
                    
                    if(col_count<32) 
                        tempLine+=",";
                }
                col_count++;
            }
            
            if(isValid) {
                fileWriter.append(tempLine);
                fileWriter.append(NEW_LINE_SEPARATOR);
            }          
            
        }
        
        fileWriter.flush();
        fileWriter.close();
       
        
    
    }
    
}
