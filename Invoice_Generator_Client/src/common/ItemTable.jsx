import React, { useState } from 'react';
import {
  Table,
  TableRow,
  TableHeaderCell,
  TableHeader,
  TableCell,
  TableBody,
  Button,
} from 'semantic-ui-react';
import InputItem from './InputItem';

function ItemTable({ items, setItems }) {
  const [modalOpen, setModalOpen] = useState(false);

//   const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({
    description: '',
    hsnCode: '',
    itemCode: '',
    qtyUnit: '',
    rate: '',
    cgst: '',
    sgst: '',
    igst: '',
    discount:''
  });

  const handleAddItem = () => {
    setItems(prev => [...prev, newItem]);
    setNewItem({
      description: '',
      hsnCode: '',
      itemCode: '',
      qtyUnit: '',
      rate: '',
      cgst: '',
      sgst: '',
      igst: '',
      discount:''
    });
    setModalOpen(false);
  };

  return (
    <div>
      <Table celled>
        <TableHeader>
          <TableRow>
            <TableHeaderCell>Description</TableHeaderCell>
            <TableHeaderCell>HSN/SAC Code</TableHeaderCell>
            <TableHeaderCell>Item Code</TableHeaderCell>
            <TableHeaderCell>Qty & Unit</TableHeaderCell>
            <TableHeaderCell>Rate</TableHeaderCell>
            <TableHeaderCell>CGST</TableHeaderCell>
            <TableHeaderCell>SGST</TableHeaderCell>
            <TableHeaderCell>IGST</TableHeaderCell>
            <TableHeaderCell>Total Discount</TableHeaderCell>
          </TableRow>
        </TableHeader>

        <TableBody>
          {items.map((item, index) => (
            <TableRow key={index}>
              <TableCell>{item.description}</TableCell>
              <TableCell>{item.hsnCode}</TableCell>
              <TableCell>{item.itemCode}</TableCell>
              <TableCell>{item.qtyUnit}</TableCell>
              <TableCell>{item.rate}</TableCell>
              <TableCell>{item.cgst}</TableCell>
              <TableCell>{item.sgst}</TableCell>
              <TableCell>{item.igst}</TableCell>
              <TableCell>{item.discount}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Button primary onClick={() => setModalOpen(true)}>Add Item</Button>

      <InputItem
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSave={handleAddItem}
        item={newItem}
        setItem={setNewItem}
      />
    </div>
  );
}

export default ItemTable;
