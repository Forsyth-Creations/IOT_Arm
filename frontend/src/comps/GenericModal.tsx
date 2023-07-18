import React, { useState } from 'react';
import { BsXSquare } from 'react-icons/bs'

interface MyComponentProps {
  showModal: boolean;
  setShowModal: (showModal: boolean) => void;
  children: React.ReactNode;
  className: string
}

const Modal: React.FC<MyComponentProps> = ({  showModal, 
                  setShowModal, 
                  children, 
                className}) => {

  // Close Modal Handler
  const closeModal = () => {
    setShowModal(false);
  };


  return (
    <>
      {showModal ? (<div className="modal-window">
            <div className="modalWindow" >
              <div className="flex flex-row">
                <div className="icon_button" onClick={closeModal}><BsXSquare></BsXSquare></div>
              </div>
              <div className= {"flex flex-col m-2 " + className}>
              {children}
              </div>
            </div>
          </div>
      ) : null}
    </>
  );
};

export default Modal;