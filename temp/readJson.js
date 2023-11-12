const fs = require('fs');

const filePath = 'convertcsv.json';

const GENERAL = "ಜನರಲ್ | General: Rs. 400/-"
const GENERAL2 = "General: Rs. 400/-"

const COLUMNS =  {
    name : "B",
    email : "K",
    universityId : "C",
    contact : "E",
    ttype : "F"
}

fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }

  try {
    const jsonData = JSON.parse(data);
    const newJsonData = [];
    jsonData.forEach(element => {
        newJsonData.push(
            {
                name : element[COLUMNS.name],
                email : element[COLUMNS.email],
                universityId : element[COLUMNS.universityId],
                contact : element[COLUMNS.contact],
                ttype : (element[COLUMNS.ttype]===GENERAL ||element[COLUMNS.ttype]===GENERAL2 )?"GA":"VIP"
            }
        )
    });
    console.log(newJsonData);
    fs.writeFile(filePath, JSON.stringify(newJsonData), 'utf8', (err) => {
        if (err) {
          console.error('Error writing the file:', err);
        } else {
          console.log('Data has been saved to', filePath);
        }
      });
  } catch (error) {
    console.error('Error parsing JSON:', error);
  }
});
