# Integra Blockchain Authenticated Smart Document Package

This package will allow the generation of Integra blockchain authenticated smart documents. The package was developed by Integra for making the generations of smart documents from DocAssemble easy and allow customizable metadata to be stored in these smart documents. The file that is created will have the hash of the document registered on the Integra blockchain and will also embed a QR code for authenticity purposes.

This package provides a function **generate()** which returns an Integra authenticated smart document from a the pdf file created by the interview and will also embed the metadata passed into the function within the pdf before the document is hashed and registered on the Integra blockchain.

For more information about Integra's blockchain authenticated smart documents please visit [Integra's Homepage](https://www.integraledger.com)

### - Function Definition

_generate(file_url, meta_data)_

> file_url - the name or variable of the file created from the interview
> meta_data - JSON representation of the fields to be embedded as metadata within the document. These field values are variables from the interview

### - Example Interviews

[Example Interview #1 - using attachment specifier](http://integra.eastus.cloudapp.azure.com/interview?i=docassemble.playground1%3Anative_docassemble.yml)

[Example Interview #2 - allowing user to upload PDF](http://integra.eastus.cloudapp.azure.com/interview?i=docassemble.playground1%3Asmartdocment.yml)

[Example Interview #3 - advanced interview](http://integra.eastus.cloudapp.azure.com/interview?i=docassemble.playground1%3Aadvanced.yml)

### - Function Usage Example - Basic

```python
generate(file, {
  "name": name,
  "color": color,
  "band": band
})
```

### - Function Usage Example - Advanced

```python
generate(demand_letter.pdf, {
    "client_name": client.name.full(),
    "client_address": client.address.on_one_line(),
    "opposing_party_name": opposing_party.name.text,
    "opposing_party_address": opposing_party.address.on_one_line(),
    "act_date": act_date.format(),
    "act_description": act_description,
    "act_harm": act_harm,
    "act_cost": currency(act_cost)
})
```

## Source Code

### - Example Interview #1 - using attachment specifier

```yaml
modules:
  - SmartDocument
---
mandatory: true
question: Step 1
subquestion: |
  Would you like to learn more about the Docassemble Integra blockchain authenticated smart documents?
buttons:
  - Yes: continue
  - No: exit
---
mandatory: true
question: Step 2
subquestion: |
  An Integra blockchain authenticated smart document stores the metadata created from this interview within the PDF and registers a hash of the document on the Integra blockchain.  No private data or information about the document is stored on the blockchain, just a digital fingerprint of the final document.
continue button label: Next
field: intro_screen
---
mandatory: true
question: Step 3
subquestion: |
  First step in creating a smart document is to have an interview that collects data, so let’s add some fields to the interview to demonstrate:
fields:
  - Name: name
  - Favorite Color: color
  - Favorite Band: band
---
mandatory: true
question: Step 4
subquestion: |
  Now that we have explained what an Integra blockchain authenticated smart document consists of, let’s create one and allow verification and authenticity of the document.
continue button label: Create Document Button
continue button field: middle_screen
---
attachment:
  - name: Integra Docassemble Example
    filename: example_letter
    variable name: example_letter
    content: |
      # Integra Docassemble Smart Document Example
      ${today()}
      Hi ${name},
      This is an example of an Integra Smart Document assembled using Docassemble.
      Included in this document will be the metadata that will include:
      > name: ${name}
      > color: ${color}
      > band: ${band}
      The final document hash will be registered on the Integra Ledger Blockchain and this document can be verified as authentic using an API call.  Once it has been verified as authentic, the meta data contained within the document will become computable and used by an existing system to injest the information contained within the document into the system.  
      This is a quick example of document automation.  For more information please visit [Integra's Homepage](https://www.integraledger.com).
      Sincerely,
      Integra Development Team
---
mandatory: True
question: Step 5
subquestion: |
  Below is a link to the Integra blockchain authenticated document that was created using the Docassemble plugin.  Once it is downloaded, you can verify the authenticity of the document by either scanning the QR code or simply clicking on it.  The verification process will require the current document to be dragged onto the screen to get the current fingerprint of the document.  Once you have verified the authenticity of the document, you can see the data contained within the document by going to 
  [https://multisign.integraledger.com/#/check-document](https://multisign.integraledger.com/#/check-document) 
  and dragging and dropping the document onto the screen.  Once it has been verified as authentic, in the upper right-hand corner will be a button that says “Metadata Viewer”.  When this button is clicked the contents of the file, stored within the metadata, will be displayed.  
  If there are additional questions or more information is required, please visit [https://www.integraledger.com](https://www.integraledger.com).

  You can download your document in
  [PDF](${ generate(example_letter.pdf, {
    "name": name,
    "color": color,
    "band": band
  }) })
buttons:
  - Finish: exit
---

```

### Example Interview #2 - allowing user to upload PDF

```yaml
modules:
  - SmartDocument
---
mandatory: true
question: Step 1
subquestion: |
  Would you like to learn more about the Docassemble Integra blockchain authenticated smart documents?
buttons:
  - Yes: continue
  - No: exit
---
mandatory: true
question: Step 2
subquestion: |
  An Integra blockchain authenticated smart document stores the metadata created from this interview within the PDF and registers a hash of the document on the Integra blockchain.  No private data or information about the document is stored on the blockchain, just a digital fingerprint of the final document.
continue button label: Next
field: intro_screen
---
mandatory: true
question: Step 3
subquestion: |
  First step in creating a smart document is to have an interview that collects data, so let's add some fields to the interview to demonstrate:
fields:
  - Name: name
  - Favorite Color: color
  - Favorite Band: band
---
mandatory: true
question: Step 4
subquestion: |
  Now that we have explained what an Integra blockchain authenticated smart document consists of, let's create one and allow verification and authenticity of the document.
continue button label: Create Document Button
continue button field: middle_screen
---
question: Step 5
subquestion: |
  Please upload a document to sign.
fields:
  - Pdf: file
    datatype: file
---
mandatory: True
question: Step 6
subquestion: |
  Below is a link to the Integra blockchain authenticated document that was created using the Docassemble plugin.  Once it is downloaded, you can verify the authenticity of the document by either scanning the QR code or simply clicking on it.  The verification process will require the current document to be dragged onto the screen to get the current fingerprint of the document.  Once you have verified the authenticity of the document, you can see the data contained within the document by going to  

  [https://multisign.integraledger.com/#/check-document](https://multisign.integraledger.com/#/check-document)   

  and dragging and dropping the document onto the screen.  Once it has been verified as authentic, in the upper right-hand corner will be a button that says "Metadata Viewer".  When this button is clicked the contents of the file, stored within the metadata, will be displayed.  


  If there are additional questions or more information is required, please visit [https://www.integraledger.com](https://www.integraledger.com).  


  You can download your document in
  [Integra Smart Document PDF](${ generate(file, {
    "name": name,
    "color": color,
    "band": band
  }) })  

  Make sure you click on the link above labeled **"Integra Smart Document PDF"** before you click on the "Finish" button below
buttons:
  - Finish: exit
---

```

### Example Interview #3 - advanced interview

```yaml
---
comment: |
  This annotated Docassemble interview shows how to assemble a document.

  There are four ways to create a document built-in to Docassemble:
  1. Create a document "from scratch" using Docassemble's formatting commands
  2. Fill in a PDF template using form fields added with Adobe Acrobat
  3. Fill in a Word Docx template using mail-merge fields (uncommon)
  4. Fill in a Word Docx template using Docassemble's special formatting tags.
  For simplicity this interview will only demonstrate the 1st method. There is
  slightly different syntax for the other options, but they offer you the ability
  to automate highly formatted documents in comparison to the demonstrated
  feature.
  This interview includes a brief example of the use of the Individual and Address 
  objects and Google Maps geocoding. It also incidentally introduces signatures,
  the currency() function, and the show if question modifier.
---
metadata:
  title: |
    Consumer Protection Demand Letter
---
comment: |
  The modules block allows you to include optional Docassemble features.
  see: https://docassemble.org/docs/initial.html#modules
modules:
  - docassemble.base.util
  - SmartDocument
---
comment: |
  The objects block allows you to make use of object-oriented classes. This is a very powerful feature
  but you can get by with just a little understanding of it.
  See: https://docassemble.org/docs/objects.html and https://www.nonprofittechy.com/2018/09/12/object-oriented-programming-for-document-assembly-developers/
objects:
  - client: Individual # Creates a new variable named client, which is an instance of an Individual object
  - opposing_party: Person # A Person represents a legal person, which might be a company rather than an individual
---
comment: |
  It's a good idea, but not required, to control the order of questions in your interview
  with a single mandatory code block like this one.
  Just list the variables that you want Docassemble to find, in order. If a screen defines more than
  one variable you only need to list one variable from that screen.
  See: https://docassemble.org/docs/logic.html#order
  You can also include Python code here but usually should only use "if" statements that control interview flow.
  See: https://github.com/GBLS/docassemble-workinggroup/blob/master/Skillshares/2.%20adding%20in%20logic/basic_logic.md
mandatory: True
code: |
  intro_screen
  client.name.first
  opposing_party.name.text
  op_business
  if not op_doing_business:
    not_doing_business
  client.address.address
  client.address.geolocate()
  right_address
  download_screen
---
decoration: user-shield
question: |
  Consumer Protection Demand Letter
subquestion: |
  This interview will help you generate a consumer protection demand
  letter, pursuant to G.L. c. 93A.

  This is an example only, and leaves out many key protections that a real
  interview would use.
field: intro_screen
---
question: |
  What is your name?
fields:
  - First name: client.name.first
  - Middle name: client.name.middle
    required: False
  - Last name: client.name.last
---
question: |
  Who do you have a consumer complaint about?
fields:
  - Name: opposing_party.name.text
---
question: |
  What is your address?
fields:
  - Address: client.address.address
    address autocomplete: True
  - Unit: client.address.unit
    required: False
  - City: client.address.city
  - State: client.address.state
    default: "MA"
    code: |
      states_list() # See https://docassemble.org/docs/functions.html#states_list
  - Zip: client.address.zip
---
question: |
  What is ${opposing_party}'s address?
fields:
  - Address: opposing_party.address.address
    address autocomplete: True
  - Unit: opposing_party.address.unit
    required: False
  - City: opposing_party.address.city
  - State: opposing_party.address.state
    default: "MA"
    code: |
      states_list() # See https://docassemble.org/docs/functions.html#states_list
  - Zip: opposing_party.address.zip
---
question: |
  Your addresses
subquestion: |
  Here's a map showing both you and ${opposing_party}.

  ${ map_of(client, opposing_party)}
field: right_address
comment: |
  The map_of() function can display a Google Map of one or more addresses or
  Individuals that have an address attached to them. See https://docassemble.org/docs/functions.html#map_of
---
question: |
  Is ${opposing_party} "in business"?
subquestion: |
  Check any true statements below.
fields:
  - ${opposing_party} is someone who offers services or sells goods for money.: op_business
    datatype: yesno
  - ${opposing_party} is a landlord.: op_landlord
    datatype: yesno
  - ${opposing_party} is a government agency or a housing authority.: op_ha
    datatype: yesno
    show if: op_landlord
  - ${opposing_party} lives in my building.: op_lives_with_me
    datatype: yesno
    show if: op_landlord
  - My building has 4 or fewer units.: small_building
    datatype: yesno
    show if: op_lives_with_me
comment: |
  You can add follow-up questions inside a single screen with the show if
  question modifier.  https://docassemble.org/docs/fields.html#show%20if
  Be careful when using this, as your user can get caught in a loop
  if a field that the interview needs is hidden behind a show if.
---
code: |
  # Here we evaluate the question above to decide if c. 93A applies.
  # It's OK to break up a Python statement into multiple lines if its enclosed 
  # by parentheses as shown below
  op_doing_business = (op_business and not op_landlord) or (
    (op_landlord and not op_ha and not op_lives_with_me) or (
      op_landlord and not op_ha and op_lives_with_me and not small_building))
---
decoration: hand-paper
event: not_doing_business
question: |
  This is the wrong interview for you.
subquestion: |
  It doesn't look like you had a business relationship with ${opposing_party}.
---
question: |
  What is the wrongful act that ${opposing_party} committed?
fields:
  - On (select date): act_date
    datatype: date
  - ${opposing_party} did this: act_description
    datatype: area
  - Because of what ${opposing_party} did, I suffered this harm: act_harm
    datatype: area
  - A fair amount of money to compensate me is: act_cost
    datatype: currency
---
question: |
  Sign your name
signature: client.signature
under: |
  ${client}
---
attachment:
  - name: 93A Demand letter
    filename: demand_letter
    variable name: demand_letter
    content: |
      # 93A Demand Letter
      ${client.address_block()}

      ${today()}

      ${opposing_party.address_block()}

      Dear ${opposing_party}:

      Under the provisions of Massachusetts General Laws, Chapter 93A, Section 9, I hereby make written
      demand for relief as outlined in that statute.

      On or about ${act_date}, the following unfair or deceptive trade practice occurred:

      ${act_description}

      As a result of this unfair or deceptive act or practice, I suffered injury or loss of money as follows:

      ${act_harm}

      Therefore, I hereby demand compensation in the amount of ${currency(act_cost)}.

      Chapter 93A gives you the opportunity to make a good-faith response to this letter within thirty (30) days.
      Your failure to do so-could subject you to triple damages, attorney's fees and costs if I decide to institute
      legal action.

      Sincerely,

      ${client.signature}

      ${client}
---
decoration: file-download
event: download_screen
question: |
  Your document is ready.
subquestion: |
  You can download your document in
  [PDF](${ generate(demand_letter.pdf, {
      "client_name": client.name.full(),
      "client_address": client.address.on_one_line(),
      "opposing_party_name": opposing_party.name.text,
      "opposing_party_address": opposing_party.address.on_one_line(),
      "act_date": act_date.format(),
      "act_description": act_description,
      "act_harm": act_harm,
      "act_cost": currency(act_cost)
    }) })
  or
  [RTF](${ demand_letter.rtf.url_for() })
  format.
```
