import { useState } from 'react';
import { BsXSquare } from 'react-icons/bs'

const Modal = ({  showModal, 
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