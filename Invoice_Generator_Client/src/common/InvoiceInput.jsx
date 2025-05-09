import { useState, React } from 'react'
import {
    FormInput,
    FormGroup,
    FormCheckbox,
    Button,
    Form,
} from 'semantic-ui-react'
import ItemTable from './ItemTable.jsx'
import './css/InvoiceInput.css'  // Link external CSS

const InvoiceInput = () => {
    const [items, setItems] = useState([]);
    const [formdata,setFormdata] = useState([]);
    const handleChange = (e, { name, value }) => {
        setFormdata(prev => ({ ...prev, [name]: value }));
      };
      const handleSubmit = async (e) => {
        e.preventDefault();
      
        try {
          const response = await fetch('http://127.0.0.1:8000/api/invoicegenerator/', {
            method: 'POST',
            headers: { // <-- ensure server knows PDF expected
        'Content-Type': 'application/json'
            },
            body: JSON.stringify({ formdata, items }),
          });
      
          if (!response.ok) throw new Error('Failed to generate PDF');
      
          const blob = await response.blob();
          console.log(blob)
          // Trigger file download
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'invoice.pdf';
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
        } catch (err) {
          console.error('Error downloading PDF:', err);
        }
      };

    return (
        <div className="invoice-wrapper">
            <Form className="invoice-form" >
                <FormGroup unstackable widths={2}>
                    <FormInput label='Company Name' placeholder='Company Name' name = "company_name" onChange={handleChange} />
                    <FormInput label='GSTIN' placeholder='GSTIN' name = "gstin" onChange={handleChange} />
                </FormGroup>
                <FormGroup widths={2}>
                    <Form.TextArea label='Address' placeholder='Address' name = "address" type='textarea' onChange={handleChange} />
                    <FormInput label='Phone' placeholder='Phone' name = "phone" onChange={handleChange} />
                </FormGroup>
                <FormGroup widths={2}>
                    <FormInput label='Invoice No.' placeholder='Invoice No.' name = "invoice_no" onChange={handleChange} />
                    <FormInput label='Date' placeholder='Date' type='date' name = "date" onChange={handleChange} />
                </FormGroup>
                <ItemTable items={items} setItems={setItems} />
                <Button type='submit' primary style={{ marginTop: '1rem' }} onClick={handleSubmit} >
                    Submit
                </Button>
            </Form>
        </div>
    );
};
export default InvoiceInput;  
