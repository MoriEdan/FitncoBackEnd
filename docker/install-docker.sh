#Sudo curl wget
echo " "
echo "****************************"
echo "* sudo curl wget kuruluyor *"
echo "****************************"
echo " "
apt update -y
apt install sudo curl wget -y

#Docker
echo " "
echo "****************************"
echo "* Docker kuruluyor         *"
echo "****************************"
echo " "

sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt update -y
apt-cache policy docker-ce
sudo apt install docker-ce docker-ce-cli -y