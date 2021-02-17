BLACK_BG=$(tput setab 4)
RED=$(tput setaf 1)
BLUE=$(tput setaf 4)
WHITE=$(tput setaf 2)
NC=$(tput sgr0) # No Color

pushd schemas

clear
echo -e "${BLACK_BG}${WHITE}Schema checkers for external and internal pipeline data${NC}"
echo -e "-------------------------------------------------------"
echo -e "${BLUE}https://redhatinsights.github.io/insights-data-schemas/${NC}"
echo ""
read
echo "Number of validators: ${RED}67${NC}"
read
echo "Total lines of code:  ${RED}6100${NC} (4300 tests)"
read
echo "Unit tests:           ${RED}2006${NC} (without fuzzy tests)"
read
echo "Code coverage:        ${RED}89%${NC}"
read

feh ../docs/images/parquet-factory.png
read

clear
echo -e "${BLACK_BG}${WHITE}Checking a file with one Feature report${NC}"
echo "---------------------------------------"
read
echo -e "${RED}./parquet_input_features.py -i features.json${NC}"
./parquet_input_features.py -i ../data/features.json
read


clear
echo "${BLACK_BG}${WHITE}Checking a file with multiple Feature reports${NC}"
echo "---------------------------------------------"
read
echo "${RED}./parquet_input_features.py -m -i features.txt${NC}"
./parquet_input_features.py -m -i ../data/last10_features.txt
read


clear
echo "${BLACK_BG}${WHITE}Checking a file with one Rule hit report${NC}"
echo "----------------------------------------"
read
echo "${RED}./parquet_input_rule_hits.py -i rule_hit.json${NC}"
./parquet_input_rule_hits.py -i ../data/rule_hits.json
read


clear
echo "${BLACK_BG}${WHITE}Checking a file with multiple Rule hit reports${NC}"
echo "----------------------------------------------"
read
echo "${RED}./parquet_input_rule_hist -m -i rule_hits.txt${NC}"
./parquet_input_rule_hits.py -m -i ../data/last10_rule_hits.txt
read


clear
echo "${BLACK_BG}${WHITE}Checking Parquet file cluster_info${NC}"
echo "----------------------------------"
read
echo "${RED}./parquet_output_cluster_info.py -i cluster_info.parquet${NC}"
./parquet_output_cluster_info.py -i ../data/cluster_info-0.parquet
read


clear
echo "${BLACK_BG}${WHITE}Checking Parquet file rule_hits${NC}"
echo "--------------------------------"
read
echo "${RED}./parquet_output_rule_hits.py -i rule_hist.parquet${NC}"
./parquet_output_rule_hits.py -i ../data/rule_hits-0.parquet
read


clear
echo "${BLACK_BG}${WHITE}Checking Parquet file cluster_thanos_info${NC}"
echo "-----------------------------------------"
read
echo "${RED}./parquet_output_thanos_info.py -i cluster_thanos_info.parquet${NC}"
./parquet_output_thanos_info.py -i ../data/cluster_thanos_info.parquet
read
