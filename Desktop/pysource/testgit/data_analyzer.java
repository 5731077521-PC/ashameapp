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
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;


/**
 *
 * @author netklause
 */
public class data_analyzer {
    
    private static final String COMMA_DELIMITER = ",";
    private static final String NEW_LINE_SEPARATOR = "\n";
    private static final String FILE_HEADER = "SrcAddr,DstAddr,Proto,Sport,Dport,"
            + "State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,"
            + "dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,"
            + "SAppBytes,DAppbytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,"
            + "DstRate,Tag";
    
    /**
     *
     */
   
   public static String[] column = {"SrcAddr","DstAddr","Proto","Sport","Dport",
       "State","sTos","dTos","SrcWin","DstWin","sHops","dHops","StartTime",
       "LastTime","sTtl","dTtl","TcpRtt","SynAck","AckDat","SrcPkts","DstPkts",
       "SrcBytes","DstBytes","SAppBytes","DAppbytes","Dur","TotPkts","TotBytes",
       "TotAppByte","Rate","SrcRate","DstRate","Tag"}; 
    
    public static int SrcAddr_column = 0;
    public static int DstAddr_column = 1;
    public static int Proto_column = 2;
    public static int Sport_column = 3;
    public static int Dport_column = 4;
    public static int State_column = 5;
    public static int sTos_column = 6;
    public static int dTos_column = 7;
    public static int SrcWin_column = 8;
    public static int DstWin_column = 9;
    public static int sHops_column = 10;
    public static int dHops_column = 11;
    public static int StartTime_column = 12;
    public static int LastTime_column = 13;
    public static int sTtl_column = 14;
    public static int dTtl_column = 15;
    public static int TcpRtt_column = 16;
    public static int SynAck_column = 17;
    public static int AckDat_column = 18;
    public static int SrcPkts_column = 19;
    public static int DstPkts_column = 20;
    public static int SrcBytes_column = 21;
    public static int DstBytes_column = 22;
    public static int SAppBytes_column = 23;
    public static int DAppbytes_column = 24;
    public static int Dur_column = 25;
    public static int TotPkts_column = 26;
    public static int TotBytes_column = 27;
    public static int TotAppByte_column = 28;
    public static int Rate_column = 29;
    public static int SrcRate_column = 30;
    public static int DstRate_column = 31;
    public static int Tag_column = 32;
    
    
    public static String fileName_read;
    public static String fileName_write;
    public static String line = "";

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, IOException {
        // TODO code application logic here
        fileName_read = "/home/netklause/Desktop/data/" + args[0];
        fileName_write = "/home/netklause/Desktop/data/" + args[1];

        
        Map collection = new HashMap();  
        
        
        BufferedReader fileReader = null;
        fileReader = new BufferedReader(new FileReader(fileName_read));
        fileReader.readLine();
        
        FileWriter fileWriter = null;
        fileWriter = new FileWriter(fileName_write);
        
        for(int i=0;i<33;i++) {
            collection.put(column[i], new HashMap<String,Integer>());
        }
        
         while ((line = fileReader.readLine()) != null) {
          
            String[] tokens = line.split(COMMA_DELIMITER);
            int col_count = 0;          
            
            //traverse column by column
            for(int i=0;i<tokens.length;i++) {
                HashMap<String,Integer> h = (HashMap<String,Integer>) collection.get(column[i]);
                
                if(h.containsKey(tokens[i])){
                    h.put(tokens[i], h.get(tokens[i]) + 1);
                }else {
                    h.put(tokens[i], 1);
                }
                
                collection.put(column[i], h);
            }
            
         }
         
         for(int i=0;i<column.length;i++) {   
             
             fileWriter.append(column[i]);
             fileWriter.append("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||");
             fileWriter.append(NEW_LINE_SEPARATOR);
             
             Map<String, String> treeMap = new TreeMap<String, String> ((Map) collection.get(column[i]));
             Set set = treeMap.entrySet();
             Iterator itr = set.iterator();
             
             while(itr.hasNext()) {
                  Map.Entry entry=(Map.Entry)itr.next(); 
                  fileWriter.append((CharSequence) entry.getKey());
                  fileWriter.append(",");
                  fileWriter.append(Integer.toString((int) entry.getValue()));
                  fileWriter.append(NEW_LINE_SEPARATOR);
                  //System.out.println(entry.getKey()+" "+entry.getValue()); 
             }
             
             fileWriter.append(NEW_LINE_SEPARATOR);
             fileWriter.append(NEW_LINE_SEPARATOR);

         }
    }
    
}
