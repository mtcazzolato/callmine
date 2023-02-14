# CallMine  

**CallMine: Fraud Detection and Visualization of Million-Scale Call Graphs**  


**Authors:** Mirela Cazzolato<sup>1,2</sup>, Saranya Vijayakumar<sup>1</sup>, Meng-Chieh Lee<sup>1</sup>, Catalina Vajiac<sup>1</sup>, Xinyi Zheng<sup>1</sup>, Namyong Park<sup>1</sup>, Pedro Fidalgo<sup>3,4</sup>, Bruno Lages<sup>3</sup>, Agma J. M. Traina<sup>2</sup>, Christos Faloutsos<sup>1</sup>\\  

**Affiliations:**  <sup>1</sup> Carnegie Mellon University (CMU), <sup>2</sup> University of São Paulo (USP), <sup>3</sup> Mobileum, <sup>4</sup> ISCTE-IUL  

*Work under review.*    

## Setup environment  

```
pip install -r requirements.txt
```
or  
```
make prep
```

## Usage:  

```
make demo
```

to see a demo of CallMine and CallMine-Focus  

## Sample Dataset:  

File 'INPUT_DATA/sample_raw_data.csv'  

**Sample size: 11,000 calls:**  
 - 10,000 random calls:  
	 - 2,000 sources  
	 - 2,000 destinations  
	 - 5 days  

	*Plus*  
- Cluster with 1,000 calls:  
	- 10 sources  
	- 10 destinations  
	- Phone calls with duration between 20 and 40 seconds  

