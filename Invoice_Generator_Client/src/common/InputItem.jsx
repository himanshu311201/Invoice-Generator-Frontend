import React from 'react';
import {
  Modal,
  ModalHeader,
  ModalContent,
  ModalDescription,
  ModalActions,
  Button,
  Icon,
  Form,
  FormInput,
  FormGroup
} from 'semantic-ui-react';

const InputItem = ({ open, onClose, onSave, item, setItem }) => {
  const handleChange = (e, { name, value }) => {
    setItem(prev => ({ ...prev, [name]: value }));
  };

  return (
    <Modal open={open} onClose={onClose}>
      <ModalHeader>Add Item</ModalHeader>
      <ModalContent>
        <ModalDescription>
          <Form>
            <FormInput
              label='Item Description'
              name='description'
              value={item.description}
              onChange={handleChange}
              placeholder='Item description'
            />
            <FormGroup widths='equal'>
            <FormInput
              label='HSN/SAC Code'
              name='hsnCode'
              value={item.hsnCode}
              onChange={handleChange}
              placeholder='HSN/SAC Code'
            />
            <FormInput
              label='Item Code'
              name='itemCode'
              value={item.itemCode}
              onChange={handleChange}
              placeholder='Item Code'
            />
            <FormInput
              label='Qty & Unit'
              name='qtyUnit'
              value={item.qtyUnit}
              onChange={handleChange}
              placeholder='Qty & Unit'
            />
            </FormGroup>
            <FormGroup widths='equal'>
            <FormInput
              label='Rate'
              name='rate'
              value={item.rate}
              onChange={handleChange}
              placeholder='Rate'
            />
            <FormInput
                label='Discount'
                name='discount'
                value={item.discount}
                onChange={handleChange}
                placeholder='Discount'
              />
            </FormGroup>
            <FormGroup widths='equal'>
              <FormInput
                label='CGST'
                name='cgst'
                value={item.cgst}
                onChange={handleChange}
                placeholder='CGST'
              />
              <FormInput
                label='SGST'
                name='sgst'
                value={item.sgst}
                onChange={handleChange}
                placeholder='SGST'
              />
              <FormInput
                label='IGST'
                name='igst'
                value={item.igst}
                onChange={handleChange}
                placeholder='IGST'
              />
            </FormGroup>
          </Form>
        </ModalDescription>
      </ModalContent>
      <ModalActions>
        <Button onClick={onSave} primary>
          Add Item <Icon name='check' />
        </Button>
        <Button onClick={onClose} secondary>
          Cancel
        </Button>
      </ModalActions>
    </Modal>
  );
};

export default InputItem;
