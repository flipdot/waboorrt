import { FormEvent } from 'react';
import styled from 'styled-components';
import useSWR from 'swr';
import Button from '../Button';
import Headline from '../Headline';
import Input from '../Input';

import PageWrapper from '../PageWrapper';

const Label = styled.span`
  display: block;
  padding-right: 20px;
  margin-bottom: 5px;
`;

const FormWrapper = styled.label`
  display: block;
  align-items: center;
  margin-bottom: 20px;
`;

const PublicKeyInput = styled(Input)`
  resize: none;
  height: 100px;
`;

export default function NewBotPage() {
  const { data: templateData } = useSWR('/api/templates');

  if (!templateData) {
    return null;
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);

    const body = {
      name: formData.get('name'),
      template: formData.get('template'),
      pubkey: formData.get('pubkey'),
    };

    console.log(body);
  }

  return (
    <PageWrapper>
      <Headline>Create Bot</Headline>
      <form onSubmit={onSubmit}>
        <div style={{ display: 'flex' }}>
          <FormWrapper style={{ flex: '1 1 auto', marginRight: '20px' }}>
            <Label>Name</Label>
            <Input $fullWidth name="name" required />
          </FormWrapper>
          <FormWrapper style={{ width: '30%' }}>
            <Label>Template</Label>
            <Input $fullWidth as="select" name="template" required>
              {templateData.map((item: string) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </Input>
          </FormWrapper>
        </div>
        <FormWrapper>
          <Label>SSH Public Key</Label>
          <PublicKeyInput
            as="textarea"
            placeholder="Begins with 'ssh-rsa' or 'ssh-ed25519'"
            name="pubkey"
            required
            $fullWidth
            style={{}}
          />
        </FormWrapper>
        <Button>Create</Button>
      </form>
    </PageWrapper>
  );
}
