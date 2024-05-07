// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;
contract MyEstate{
  enum EstateType { House, Flat, Loft }
  enum AdStatus { Opened, Closed }
  // Недвижимость
  // Площадь
  // Адрес
  // Владелец
  // ID недвижимости
  // Тип дом кв лофт
  // Статус активно или нет 
  struct Estate{
    uint size;
    string estateAddress;
    address owner;
    EstateType esType;
    bool isActive;
    uint idAstate;
  }
  // Обьявление
  //Продавец
  // Покупатель
  // Стоимость
  //ID недвижимости
  // Дата сощдания
  // Статус открыто или закрыто

  struct Advertisement{
    address owner;
    address buyer;
    uint price;
    uint idEstate;
    uint dateTime;
    AdStatus isOpen;
  }

  Estate[] public estates;
  Advertisement[] public ads;

  mapping (address=>uint) public balances;
// функционал:
// Создание объявления
// Создание объявления
// Смена статуса недвижимости
// Смена статуса объявления
// Снятие средств со смарт контракта
// Покупка недвижимости
// Получение баланса

  event estateCreated(address owner, uint idEstate, uint dateTime, EstateType estateType);
    event adCreated(address owner, uint idEstate, uint idAd, uint dateTime, uint price);
    event estateStatusChanged(address owner, uint idEstate, uint dateTime, bool status);
    event adStatusChanged(address owner, uint idEstate, uint idAd, uint dateTime, bool status);
    event estatePurchased(address buyer, address owner, uint idEstate, uint idAd, uint dateTime, uint price);
    event fundsBack(address recipient, uint amount, uint dateTime);



  modifier enoughValue(uint value, uint price){
    require(value >= price, unicode"У вас недостаточно средст");
    _;
  }

  modifier onlyEstateOwner(uint idEstate){
    require(estates[idEstate].owner == msg.sender, unicode"Вы не владелец данной недвижимости");
    _;
  }
  modifier onlyAdOwner(uint idAd){
    require(ads[idAd].owner == msg.sender, unicode"Вы не владелец данного обьявления");
    _;
  }

  modifier isActiveEstate(uint idEstate){
    require(estates[idEstate].isActive, unicode"Данная недвижимость недоступна");
    _;
  }

  modifier isClosedAd(uint idAd){
    require(ads[idAd].isOpen == AdStatus.Opened, unicode"Данное обьявление закрыто");
    _;
  }
  
  function createEstate(uint _size, string memory _estateAddress, EstateType _estateType) public {
    require(_size >= 1, unicode"Размер должty быть больше 0");
    uint id = estates.length;
     estates.push(Estate({
        size: _size,
        estateAddress: _estateAddress,
        owner: msg.sender,
        esType: _estateType,
        isActive: true,
        idAstate: id
    }));
    emit estateCreated(msg.sender, id, block.timestamp, _estateType);
  }
  function createAd(address buyer, uint sum, uint _idEstate) public onlyEstateOwner(_idEstate) isActiveEstate(_idEstate) {
    require(buyer != address(0), unicode"Неверный пользователь");
    require(sum > 0, unicode"Сумма должна быть больше 9");
    ads.push(Advertisement({
        owner: msg.sender,
        buyer: buyer,
        price: sum,
        idEstate: _idEstate,
        dateTime: block.timestamp,
        isOpen: AdStatus.Opened
    }));
    emit adCreated(msg.sender, _idEstate, ads.length, block.timestamp, sum);
  }


   function changesStatusEstate(uint _idEstate, bool _status) public onlyEstateOwner(_idEstate) {
        estates[_idEstate].isActive = _status;
        emit estateStatusChanged(msg.sender, _idEstate, block.timestamp, _status);
        if (!_status) {
            for (uint i = 0; i < ads.length; i++) {
                if (ads[i].idEstate == _idEstate && ads[i].isOpen == AdStatus.Opened) {
                    ads[i].isOpen = AdStatus.Closed;
                    emit adStatusChanged(msg.sender, _idEstate, i, block.timestamp, false);
                }
            }
        }
    }

  function changestatusAd(uint _idAd, bool _status) public onlyEstateOwner(ads[_idAd].idEstate) {
        ads[_idAd].isOpen = _status ? AdStatus.Opened : AdStatus.Closed;
        emit adStatusChanged(msg.sender, ads[_idAd].idEstate, _idAd, block.timestamp, _status);
    }

    function withDraw(uint _amount) public payable{
        require(_amount > 0 && _amount <= address(this).balance, unicode"Неверная сумма для вывода");
        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
        emit fundsBack(msg.sender, _amount, block.timestamp);
    }

  function getBalance() public view returns(uint) {
        return balances[msg.sender];
    }

    function getEstates() public view returns(Estate[] memory) {
        return estates;
    }

    function getAds() public view returns(Advertisement[] memory) {
        return ads;
    }

    function deposit(uint _amount) public payable {
    require(_amount > 0, unicode"Неверная сумма для пополнения");
    balances[msg.sender] += _amount;
}

   function buyEstate(uint idAd) public payable isClosedAd(idAd) {

    require(msg.value >= ads[idAd].price, unicode"Недостаточно средств для покупки");
    require(ads[idAd].owner != msg.sender, unicode"Владелец не может быть покупателем");
    uint idEstate = ads[idAd].idEstate;

    address payable seller = payable(estates[idEstate].owner);
    seller.transfer(ads[idAd].price);
    balances[seller] += ads[idAd].price;

    balances[msg.sender] -= ads[idAd].price;

    estates[idEstate].owner = msg.sender;

    ads[idAd].isOpen = AdStatus.Closed;
    emit estatePurchased(msg.sender, seller, idEstate, idAd, block.timestamp, ads[idAd].price);
    emit adStatusChanged(msg.sender, idEstate, idAd, block.timestamp, false);
}
}      
